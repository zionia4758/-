#include <stdio.h>
#include <stdlib.h>
//2016025196_김동규_알고리즘문제해결기법

typedef struct link
{
	int w;
	int a;
	link* next;
}link;
typedef struct node
{
	int num;
	link* next;
	int count;
	int weight;
	link* tail;
}node;
node** N;
node** Q;
void relaxation(int count, int* arr)
{
	link* next;
	int newW;
	//for (int i = 1; i <= 4; ++i)printf("%d ", arr[i]);
	
		next = Q[count]->next;
		for (int j = 0; j < Q[count]->count; ++j)
		{
			//printf("\n%d %d", arr[next->a], next->a);
			if (arr[next->a] == 1) {
				next = next->next;
				continue;
			}

			newW = next->w + Q[count]->weight;
			if (newW < N[next->a]->weight)
				N[next->a]->weight = newW;
			next = next->next;
		}

}
int Dijkstra(int n)
{
	Q = (node**)malloc((n + 1)* sizeof(node*));
	int count = 1;
	int* arr = (int*)calloc(n + 1, sizeof(int));
	int select;
	int weight;
	int swtch;
	Q[1] = N[1];
	arr[1] = 1;	
	for (; count<= n;count++ )
	{
		//
		swtch = 0;
		weight = 9876543;
		select = -1;
		relaxation( count,arr);
		for (int i = 2; i <= n; ++i)
		{
			if (arr[i] == 1) continue;
			if (N[i]->weight < weight)
			{
				swtch = 1;
				weight = N[i]->weight;
				select = i;
			}
		}
		if (swtch == 0) break;

		

		Q[count+1] = N[select];
		arr[select] = 1;
	}
	
	int result = 0;
	for (int i = 2; i <= count; ++i)
	{
		if (Q[i]->weight > result)
			result = Q[i]->weight;
	}
	return result;
}



int main()
{
	int n, m;
	int a, b, w;
	//int size = 0;

	scanf("%d %d ", &n, &m);
	N = (node**)calloc(n+1,sizeof(node*));
	//size += sizeof(node*) * (n + 1);
	for (int i = 1; i <= n; ++i)
	{
		N[i] = (node*)calloc(1, sizeof(node));
		N[i]->next = (link*)calloc(1, sizeof(link));
		N[i]->num = i;
		N[i]->weight = 98765421;
		N[i]->tail = N[i]->next;
	
	}	//size += sizeof(node) * (n + 1) + 80;
	N[1]->weight = 0;
	for (int i = 0; i < m; ++i)
	{
		scanf("%d %d %d", &a, &b,&w);
		N[a]->tail->w = w;
		N[a]->tail->a = b;
		N[a]->tail->next = (link*)calloc(1, sizeof(link));
		N[a]->tail = N[a]->tail->next;
		N[a]->count++;
	}
	

//	printf("%d", size);
	printf("%d\n", Dijkstra(n));
	//Dijkstra(n);
	//Dijkstra(n);

	int result = 0;
	
	//printf("%d\n", result);
	/*
	for (int i = 1; i <= n; ++i)
	{

		free(N[i]);
	}
	free(Q);
	free(N);*/
}