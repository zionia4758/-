#include "sched.h"


#define MAX_COUNT 4

static void put_prev_task_myrr(struct rq *rq, struct task_struct *p);
static int select_task_rq_myrr(struct task_struct *p, int cpu, int sd_flag, int flags);
static void set_curr_task_myrr(struct rq *rq);
static void task_tick_myrr(struct rq *rq,struct task_struct *p, int oldprio);
static void switched_to_myrr(struct rq *rq, struct task_struct *p);
void init_myrr_rq(struct myrr_rq *myrr_rq);
static void update_curr_myrr(struct rq *rq);
static void enqueue_task_myrr(struct rq *rq, struct task_struct *p, int flags);
static void dequeue_task_myrr(struct rq *rq, struct task_struct *p, int flags);
static void check_preempt_curr_myrr(struct rq *rq, struct task_struct *p,int flags);
struct task_struct *pick_next_task_myrr(struct rq *rq, struct task_struct *prev);
static void prio_changed_myrr(struct rq *rq, struct task_struct *p, int oldprio);


const struct sched_class myrr_sched_class={
	.next=&fair_sched_class,
	.enqueue_task=&enqueue_task_myrr,
	.dequeue_task=dequeue_task_myrr,
	.check_preempt_curr=check_preempt_curr_myrr,
	.pick_next_task=pick_next_task_myrr,
	.put_prev_task=put_prev_task_myrr,
#ifdef CONFIG_SMP
	.select_task_rq=select_task_rq_myrr,
#endif
	.set_curr_task=set_curr_task_myrr,
	.task_tick=task_tick_myrr,
	.prio_changed=prio_changed_myrr,
	.switched_to=switched_to_myrr,
	.update_curr=update_curr_myrr,
};


void init_myrr_rq (struct myrr_rq *myrr_rq)
{
	printk(KERN_INFO "***[MYRR] Mysched class is online \n");
	myrr_rq->nr_running=0;
	INIT_LIST_HEAD(&myrr_rq->queue);

}
static void update_curr_myrr(struct rq *rq){
	
	/*
	현재 실행중인 태스크가 Time Slice(update num)를 모두 소진했다면
	1. 서브 런큐에서의 순서 정렬(현재 실행되고 있는것을 맨 뒤로)
	2. update num 초기화
	3. ﻿rescheduling 요청
	*/
	struct task_struct *curr=rq->curr;
	struct sched_myrr_entity *myrr_se=&curr->myrr;

	printk(KERN_INFO"update_curr pid : %d, update_num : %d\n",curr->pid,myrr_se->update_num);	
	
	if(curr->sched_class !=&myrr_sched_class)
		return;

	myrr_se->update_num++;
	if(myrr_se->update_num>MAX_COUNT)
	{
		myrr_se->update_num=0;
		list_move_tail(&myrr_se->run_list,&rq->myrr.queue);	
		printk(KERN_INFO"update_curr_myrr : resched, nr_running: %d\n",rq->myrr.nr_running);		
		resched_curr(rq);
		return ;
	}
	
	/*
	u64 delta_exec;
	delta_exec=rq_clock_task(rq) - curr->se.exec_start;
	curr->se.sum_exec_runtime+=delta_exec;
	curr->se.exec_start=rq_clock_task(rq);
	if(sched_myrr_runtime_exceeded(myrr_se))
		resched_curr(rq);
	*/
}

static void enqueue_task_myrr(struct rq *rq, struct task_struct *p, int flags) {

	/*﻿
	1. 서브 런큐에 삽입
	*/
	struct sched_myrr_entity *myrr_se=&p->myrr;
	list_add_tail( &myrr_se->run_list,&rq->myrr.queue);
	rq->myrr.nr_running++;
	printk(KERN_INFO"enqueue_task_myrr: success, cpu =%d, nr_running: %d, pid=%d\n",cpu_of(rq),rq->myrr.nr_running,p->pid);
}
static void dequeue_task_myrr(struct rq *rq, struct task_struct *p, int flags) 
{
	/*﻿
	1. 서브 런큐 dequeue 동작
	*/	
	struct sched_myrr_entity *myrr_se=&p->myrr;
	if(rq->myrr.nr_running>0)
	{
		myrr_se->update_num=0;
		list_del_init(&myrr_se->run_list);
		rq->myrr.nr_running--;
		printk(KERN_INFO"dequeue_task_myrr: success nr_running: %d, pid=%d\n",rq->myrr.nr_running,p->pid);
	}

}
void check_preempt_curr_myrr(struct rq *rq, struct task_struct *p, int flags) {
	printk(KERN_INFO"***[MYRR] check_preempt_curr_myrr\n");
}
struct task_struct *pick_next_task_myrr(struct rq *rq, struct task_struct *prev)
{
	if(rq->myrr.nr_running==0 ){
		return NULL;
	}
	struct list_head *next_head=rq->myrr.queue.next;
	struct sched_myrr_entity *next_entity;	
	struct task_struct *next_task;


	next_entity=container_of(next_head ,struct sched_myrr_entity, run_list);

	next_task=container_of(next_entity, struct task_struct, myrr);
	
	printk(KERN_INFO"pick_next_task: prev->pid=%d,next->pid=%d,nr_running=%d\n",prev->pid, next_task->pid, rq->myrr.nr_running);
	/*﻿
	1. next task를 서브 런큐에서 pick
	2. next task를 return 
	*/
	next_task->se.exec_start=rq_clock_task(rq);
	return next_task;
}
void put_prev_task_myrr(struct rq *rq, struct task_struct *p) {
	printk(KERN_INFO "\t***[MYRR] put_prev_task: do_nothing, p->pid=%d\n",p->pid);
}
int select_task_rq_myrr(struct task_struct *p, int cpu, int sd_flag, int flags){return task_cpu(p);}
void set_curr_task_myrr(struct rq *rq){
	printk(KERN_INFO"***[MYRR] set_curr_task_myrr\n");
}
void task_tick_myrr(struct rq *rq, struct task_struct *p, int queued) {
	update_curr_myrr(rq);
}
void prio_changed_myrr(struct rq *rq, struct task_struct *p, int oldprio) { }
/*This routine is called when a task migrates between classes*/
void switched_to_myrr(struct rq *rq, struct task_struct *p)
{
	resched_curr(rq);
}