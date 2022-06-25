#include <stdio.h>
#include <stdlib.h>
#pragma once
//2016025196_김동규_알고리즘문제해결기법

typedef struct Node
{
	struct Node* arr[1001];
	int count=0;
	int num;
	int color;//0=white1=gray2=black;
	int indegree = 0;
	int outdegree = 0;
}Node;
Node* node[1001];

typedef struct queue
{
	struct Node (* recent);
	struct queue (* next);
	
	
}Queue;
static Queue* head;
static Queue* tail;
static int count;
Queue* Q;
Queue* initQ()
{
	Q = (queue*)calloc(1, sizeof(queue));
	head = Q;
	tail = Q;
	count = 0;
	return Q;
}
void enqueue(Node* n)
{
	tail->recent = n;
	tail->next = (queue*)calloc(1, sizeof(queue));
	tail = tail->next;
	count++;
}
Node* dequeue()
{	
	Node* ret = head->recent;
	if (head == tail) { printf("error\n"); exit(0); }
	head = head->next;
	return ret;
}

void DFS(Node* n)
{
	if (n->indegree == 0) {
		enqueue(n); n->indegree = -1;
		printf("%d ", n->num);
	}
	for (int i = 0; i < n->count; ++i)
	{
	//	printf("%d\n",n->num);
		
			n->arr[i]->indegree--;
			DFS(n->arr[i]);
		
	}
	
}
typedef struct nodearr
{
	struct Node(*node);
	struct nodearr(*next);
	struct nodearr(*tail);
}narr;
nodearr* list;
int main()
{
	int n, m;
	int a, b;
	initQ();
	scanf("%d %d", &n, &m);	
//	list = (nodearr*)calloc(1, sizeof(nodearr));list->tail = list;
	for (int i = 1; i <= n; ++i)
	{
		node[i] = (Node*)calloc(1, sizeof(Node));
		node[i]->num = i;
	
		
	//	list->tail->node = node[i];
		//list->tail->next = (nodearr*)calloc(1, sizeof(nodearr));
	//	list->tail = list->tail->next;
	}
	for (int i = 0; i < m; ++i)
	{
		scanf("%d %d", &a, &b);
		
		node[a]->arr[node[a]->count] = node[b];		
		//printf("??? %d \n", node[a]->count);
		node[a]->count++;

		
		node[a]->outdegree++;
		node[b]->indegree++;
	}
	/*
	for (int i = 1; i <= n; ++i)
	{
		printf("%d %d %d %d\n", node[i]->indegree, node[i]->outdegree,node[i]->count, node[i]->num);
	}*/
	/*
	while(list->node!=NULL)
	{
		nodearr* temp = list;
		while (temp != NULL)
		{
			if (temp->node->indegree == 0)
				DFS(temp->node);
			temp = temp->next;
		}
		
	}*/
	for (int i = n; i > 0; --i)
	{
		int swch = 0;
		for (int i = n; i >0; --i)
		{
			if (node[i]->indegree == 0)
			{
				swch = 1;
				DFS(node[i]);
			}
				
		}
		if (swch == 0)break;
	}
		printf("1\n");
		for (int i = 0; i < n; ++i)
			printf("%d ", dequeue()->num);
	
}