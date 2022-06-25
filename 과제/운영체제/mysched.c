#include "sched.h"
void init_mysched_rq(struct mysched_rq *mysched_rq)
{
	printk(KERN_INFO "***[MYSCHED] Myschedclass is online \n");
	INIT_LIST_HEAD(&mysched_rq->queue);
}

static void update_curr_mysched(struct rq *rq)
{
}
static void enqueue_task_mysched(struct rq *rq, struct task_struct *p, int flags) 
{	
	printk("enqueue start\n");
	struct sched_mysched_entity *mysched_entity=&p->mysched;
	list_add_tail(&rq->mysched.queue,&mysched_entity->run_list);
	rq->mysched.nr_running++;
	printk("enqueue end\n");
}

static void dequeue_task_mysched(struct rq *rq, struct task_struct *p, int flags)
{
	printk("dequeue start\n");
	list_del(rq->mysched.queue.next);
	rq->mysched.nr_running--;
	printk("dequeue end\n");
}
static void check_preempt_curr_mysched(struct rq *rq, struct task_struct *p, int flags) 
{ 
}
struct task_struct *pick_next_task_mysched(struct rq *rq, struct task_struct *prev)
{	
	printk("pick_next_task start\n");

	struct sched_mysched_entity* next_entity=container_of(prev->mysched.run_list.next,struct sched_mysched_entity,run_list);
	struct task_struct* next_task=container_of(next_entity,struct task_struct,mysched);
	printk("pick_next_task: cpu=%d prev->pid=%d next_p->pid=%d nr_running=%d\n",prev->on_cpu,prev->pid,next_task->pid,rq->mysched.nr_running);

	printk("pick_next_task end\n");
	printk("next=%p,queue=%p\n",&next_task->mysched.run_list,rq->mysched.queue.next);
	if(&next_task->mysched.run_list!=&rq->mysched.queue && rq->mysched.queue.next!=0)
		return next_task;
	else
		return NULL;
}
static void put_prev_task_mysched(struct rq *rq, struct task_struct *p) 
{
 	printk("put_prev : do noting, p->pid : %d\n",p->pid);
	
}
static int select_task_rq_mysched(struct task_struct *p, int cpu, int sd_flag, int flags)
{
	return task_cpu(p);
}
static void set_curr_task_mysched(struct rq *rq) 
{ 
}
static void task_tick_mysched(struct rq *rq, struct task_struct *p, int queued) 
{ 
}
static void prio_changed_mysched(struct rq *rq, struct task_struct *p, int oldprio) 
{ 
}
/* This routine is called when a task migrates between classes */
static void switched_to_mysched(struct rq *rq, struct task_struct *p)
{
	resched_curr(rq);
}
const struct sched_class mysched_sched_class = {
	.next			= &idle_sched_class,
	.enqueue_task		= enqueue_task_mysched,
	.dequeue_task		= dequeue_task_mysched,
	.check_preempt_curr	= check_preempt_curr_mysched,
	.pick_next_task		= pick_next_task_mysched,
	.put_prev_task		= put_prev_task_mysched,

#ifdef CONFIG_SMP
	.select_task_rq		= select_task_rq_mysched,
#endif
	.set_curr_task		= set_curr_task_mysched,
	.task_tick		= task_tick_mysched,
	.prio_changed		= prio_changed_mysched,
	.switched_to		= switched_to_mysched,
	.update_curr		= update_curr_mysched,
};