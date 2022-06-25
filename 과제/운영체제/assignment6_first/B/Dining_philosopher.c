#include <stdio.h>
#include <unistd.h>
#include <semaphore.h>
#include <pthread.h>

#define COUNTING_NUMBER 30

sem_t stick[6];

void* eat(void* n)
{
	int num= *(int*)n;
	printf("%dth philosopher start\n",num);
	for(int i=0;i<COUNTING_NUMBER;++i)
	{
		if(num%2==0)
			sem_wait(&stick[num]);
		else
			sem_wait(&stick[(num+1)%6]);
		usleep(50000);
		printf("%dth philosopher's %dth eating end.\n",num,i+1);
	//	printf("put down %d,%d chopstick\n",num,(num+1)%6);
		sem_post(&stick[num]);
		sem_post(&stick[(num+1)%6]);
		usleep(50000);
	}
}



int main()
{

	int i;
	pthread_t philosopher[6];
	int p_num[6]={0,1,2,3,4,5};
	for(i=0;i<6;++i)
	{
		sem_init(&stick[i],0,1);
	}
	for(i=0;i<6;++i)
	{
		pthread_create(&philosopher[i],0,eat,(void*)&p_num[i]);
	}
	for(i=0;i<6;++i)
	{
		pthread_join(philosopher[i],0);
	}
	for(i=0;i<6;++i)
	{
		sem_destroy(&stick[i]);
	}
	return 0;
}
