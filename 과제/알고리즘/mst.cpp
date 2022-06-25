#include <stdio.h>
#include <stdlib.h>

//2016025196_김동규_알고리즘문제해결기법

typedef struct edge
{
	int a, b, weight;

}Edge;
typedef struct met
{
	int presenter;
	int next;
	int tail;
}met;
 Edge* e[500000];
 met metrix[1001];
static int index = 0;
int smallone(int a, int b)
{
	if (e[a]->weight < e[b]->weight)
		return a;
	else if (e[a]->weight == e[b]->weight)
	{
		if (e[a]->a < e[b]->a)
			return a;
		else if (e[a]->a == e[b]->a)
		{
			if (e[a]->b < e[b]->b)
				return a;
		}
	}
	return b;
}
void Min_heap_sort(int i)
{

	int right = i * 2 + 1;
	int left = i * 2;
	int small = i;
	edge* temp;
	
	if (left <= index)
	{
		small = smallone(i,left);
	}

	if (right <= index)
	{
		small = smallone(small,right);	
		
	}
	if (i == small)
		return;
	
	temp = e[small];
	e[small] = e[i];
	e[i] = temp;
	Min_heap_sort(small);
	return;

}

void Insert_heap(edge* ed)
{
	if (index == 100001)
		return;
	e[++index] = ed;
	for (int i = index; i > 0; i /= 2)
		Min_heap_sort(i);
	//just_show();
	return;

}

edge* Delete_queue()
{
	edge* result = e[1];
	if (index == 0) {
		printf("error\n"); exit(0);
	}
	e[1] = e[index];
	index--;
	Min_heap_sort(1);
	//just_show();
	return result;
}

void unionset(int  to,int from)
{
	int a = metrix[to].presenter;
	int link = metrix[from].next;
	



	metrix[from].presenter = metrix[to].presenter;
	metrix[from].tail = metrix[to].tail;
	while (link != 0)
	{
		metrix[link].presenter = metrix[to].presenter;
		link = metrix[link].next;
		metrix[link].tail = metrix[to].tail;
	}
	metrix[metrix[from].tail].next = metrix[to].next;
	metrix[to].next = from;
		if (metrix[to].tail == 0) metrix[to].tail = from;
}
int main()
{
	int n;
	int m;
	int a, b, weight;
	int mask[1001] = { 0 };
	int count; int k = 0;
	scanf("%d %d", &n, &m);
	
	//e = (edge**)calloc(n+1, sizeof(edge*));
	for (int i = 1; i <= n; ++i)
	{
		metrix[i].presenter=i;
		//metrix[i].tail = i;
	}
	for (int i = 0; i < m; ++i)
	{
		scanf("%d %d %d", &a, &b, &weight);
		if (b < a)
		{
			int temp = a;
			a = b;
			b = temp;
		}
		edge* ed= (edge*)calloc(1,sizeof(edge));
		ed->a = a;
		ed->b = b;
		ed->weight = weight;

		Insert_heap(ed);
	}
	printf("%d\n", n-1);
	count = 0;
	/*
	while (index > 0) {
		edge* ed = Delete_queue();
		printf("%d %d %d %d\n", ed->a, ed->b, ed->weight, ed->presenter);
	}*/
	while (index >= 1)
	{
		edge* ed = Delete_queue();
		if (mask[ed->a] == 0) {
			mask[ed->a] = 1;
			count++;
		}
		if (mask[ed->b] == 0) {
			mask[ed->b] = 1;
			count++;
		}
		if (metrix[ed->a].presenter != metrix[ed->b].presenter)
		{
		
			if (metrix[ed->a].presenter <= metrix[ed->b].presenter)
				unionset(ed->a, ed->b);
			else
				unionset(ed->b, ed->a);
			for (int i = 1; i <= n;++i)
				printf("%d pre: %d next:%d tail: %d\n",i, metrix[i].presenter, metrix[i].next,metrix[i].tail);
			printf("%d %d %d\n", ed->a, ed->b, ed->weight);
		}
		
	}
	//for (int i = 0; i <= n; ++i)
	//	free(e[i]);
	
	//free(e);


}