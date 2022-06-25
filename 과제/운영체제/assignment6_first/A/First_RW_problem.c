#include <stdio.h>
#include <semaphore.h>
#include <pthread.h>
#include <unistd.h>
#define COUNTING_NUMBER 50

int cur_writer,cur_count;
sem_t wrt;
sem_t S;
int readcount=0;


void writer(void* n)
{
	int i;
	int num=*(int*)n;
	for(i=0;i<COUNTING_NUMBER;++i)
	{
		usleep(100000);
		sem_wait(&wrt);
		cur_writer=num;
		cur_count=i;
		sem_post(&wrt);
	}

}

void reader()
{
	int i;
	for(i=0;i<COUNTING_NUMBER;i++)
	{
		usleep(30000);
		
		sem_wait(&S);
		readcount++;
		if(readcount==1)
			sem_wait(&wrt);
		sem_post(&S);
		printf("The most recent wrt id:\t [%d] , count:\t [%d]\n",cur_writer,cur_count);
		sem_wait(&S);
		readcount--;
		if(readcount==0)
		{	
//			printf("signal to wrt\n");
			sem_post(&wrt);
		}
		sem_post(&S);

	}
}




int main()
{
	int i;
	
	sem_init(&wrt,0,1);
	sem_init(&S,0,1);
	


	pthread_t thread_writer[2],thread_reader[5];
	int num[2]={0,1};
	for(i=0;i<2;++i)
	{
		pthread_create(&thread_writer[i],NULL,(void*)&writer,(void*)(num+i));

	}
	for(i=0;i<5;++i)
	{
		pthread_create(&thread_reader[i],NULL,(void*)&reader,NULL);
	}
	for(i=0;i<2;++i)
	{
		pthread_join(thread_writer[i],NULL);

	}
	for(i=0;i<5;++i)
	{
		pthread_join(thread_reader[i],NULL);
	}
	sem_destroy(&wrt);
	sem_destroy(&S);








	return 0;
}
