
#include "sched.h"

static void enqueue_task_mystride(struct rq*rq,struct task_struct*p,int flags);
static void dequeue_task_mystride(struct rq*rq,struct task_struct*p,int flags);
static void update_curr_mystride(struct rq *rq);
static struct task_struct *pick_next_task_mystride(struct rq *rq, struct task_struct *prev);



static int select_task_rq_mystride(struct task_struct *p, int cpu, int sd_flag, int flags)
{
    return task_cpu(p);
}


void init_mystride_rq(struct mystride_rq *mystride_rq)
{
    printk(KERN_INFO "***[MYSTRIDE] Mystride class is online \n");


    mystride_rq->nr_running=0;


    INIT_LIST_HEAD(&mystride_rq->queue);

}
void init_task_mystride(struct task_struct *p)
{
	struct sched_mystride_entity *se=&p->mystride;

	p->sched_class=&mystride_sched_class;
	se->stride=1000/(se->ticket);
	se->pass =se->stride;
}
static void check_preempt_curr_mystride(struct rq *rq, struct task_struct *p, int flags) 

{ 
	resched_curr(rq);
}

static void put_prev_task_mystride(struct rq *rq, struct task_struct *p) 

{
    printk(KERN_INFO "\t***[MYSRTIDE] put_prev_task: do nothing, p->pid=%d\n", p->pid);
}



static void set_curr_task_mystride(struct rq *rq) 
{ 
}
static void task_tick_mystride(struct rq *rq, struct task_struct *p, int queued) 
{ 
	static int count=0;
	
	update_curr_mystride(rq);
	count ++;
	if(count>15)
	{	
		struct sched_mystride_entity *se;
		list_for_each_entry(se,&rq->mystride.queue,run_list)
		{
			struct task_struct* entry_task=container_of(se,struct task_struct, mystride);
			printk("Aging :pid=%d pass%d ->",entry_task->pid,se->pass);
			se->pass=se->pass*3/4;
			printk("%d\n",se->pass);
		}
		count=0;
	}
}
static void prio_changed_mystride(struct rq *rq, struct task_struct *p, int oldprio) 
{
 	dequeue_task_mystride(rq,p,0);
	enqueue_task_mystride(rq,p,0);
		

}

/* This routine is called when a task migrates between classes */


static void switched_to_mystride(struct rq *rq, struct task_struct *p)
{
    resched_curr(rq);
}

//mystride queue : where pass(priority) put in
//mystride queue=priority fifo queue
static void enqueue_task_mystride(struct rq *rq, struct task_struct *p, int flags) 
{

	int i;
	
	if(rq->mystride.nr_running==0)
	{
		list_add_tail(&p->mystride.run_list,&rq->mystride.queue);
		rq->mystride.nr_running++;
		return;
	}
		
	struct sched_mystride_entity *recent=&p->mystride;	

	struct list_head *head=rq->mystride.queue.next;
	struct sched_mystride_entity *mystride_se;

	for(i=0;i<rq->mystride.nr_running;++i)
	{
		mystride_se=container_of(head, struct sched_mystride_entity, run_list);
		if(recent->pass > mystride_se->pass)
			head=head->next;

		else 
			break;
	}	
	list_add_tail(&p->mystride.run_list, head);
	rq->mystride.nr_running++;
	printk("[MYSTRD]enqueue : pid=%d, nr_running=%d, pass=%d\n",p->pid,rq->mystride.nr_running,
		p->mystride.pass);
	//preempt
	if(head!=rq->mystride.queue.next)
	{
		printk("preempt\n");
		check_preempt_curr_mystride(rq,p ,0);
	}
		



}


static void dequeue_task_mystride(struct rq *rq, struct task_struct *p, int flags)
{

 	struct sched_mystride_entity *mystride_se=&p->mystride;
	if(rq->mystride.nr_running>0)
	{
		list_del_init(&p->mystride.run_list);
		rq->mystride.nr_running--;
	}
	printk("[MYSTRD]dequeue : nr_running=%d\n",rq->mystride.nr_running);	



}


//add stride to pass every update
static void update_curr_mystride(struct rq *rq)
{

	struct task_struct *curr=rq->curr;
	struct sched_mystride_entity  *mystride_se=&curr->mystride;

	int prev=mystride_se->pass;
	mystride_se->pass+=mystride_se->stride;
	printk("[MYSTRD]update_curr: pid=%d, pass= %d->%d\n",curr->pid,prev,
		mystride_se->pass);


	//is it still  highest prio?
	if(rq->mystride.nr_running==1)
		return;
	else
	{
		struct list_head *next_head= mystride_se->run_list.next;
		struct sched_mystride_entity *next=container_of(next_head, struct sched_mystride_entity, run_list);

		if(mystride_se->pass > next->pass)
		{
		
			printk("update_curr : resched\n");
			prio_changed_mystride(rq,curr,prev);
		}
	}
}



//return first task
struct task_struct *pick_next_task_mystride(struct rq *rq, struct task_struct *prev)
{
 
	struct task_struct *p;
	struct sched_mystride_entity *mystride_se;
	
	if(rq->mystride.nr_running==0)
		return NULL;
	else
	{
	 	mystride_se=list_entry(rq->mystride.queue.next,struct sched_mystride_entity,
					run_list);
		p=container_of(mystride_se, struct task_struct,mystride);
		
	}

	printk("pick_next_task: nr_running=%d, pid=%d, pass=%d\n",
		rq->mystride.nr_running,p->pid,p->mystride.pass);
	return p;
}





const struct sched_class mystride_sched_class = {
    .next               = &fair_sched_class,
    .enqueue_task       = enqueue_task_mystride,
    .dequeue_task       = dequeue_task_mystride,
    .check_preempt_curr = check_preempt_curr_mystride,
    .pick_next_task     = pick_next_task_mystride,
    .put_prev_task      = put_prev_task_mystride,

#ifdef CONFIG_SMP
    .select_task_rq     = select_task_rq_mystride,
#endif
    .set_curr_task      = set_curr_task_mystride,
    .task_tick          = task_tick_mystride,
    .prio_changed       = prio_changed_mystride,
    .switched_to        = switched_to_mystride,
    .update_curr        = update_curr_mystride,
};
