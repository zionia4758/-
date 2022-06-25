#include <stdio.h>
#include <stdlib.h>
//2016021596_김동규_알고리즘문제해결기법

typedef struct set
{
	int presenter;
	int number;
	set* prec;
	set* next;


}set;
set* arr[1001];
int find_set(set* set)
{
	return set->prec->presenter;
}

void union_set(set* set1, set* set2)
{
	set* temp=set2;
	while (temp != NULL)
	{
		temp->presenter = set1->presenter;
		temp->prec = set1->prec;
		temp = temp->next;
	}
	temp = set1->next;
	set1->next = set2;
}

int main()
{

	int n, m;
	int a, b;
	int ret;
	scanf("%d %d", &n, &m);
	ret = n;
	for (int i = 1; i <= n; ++i)
	{
		arr[i] = (set*)calloc(1, sizeof(set));
		arr[i]->number = i;
		arr[i]->presenter=i;

		arr[i]->prec = arr[i];
		
	}
	for (int i = 0; i < m; ++i)
	{
		scanf("%d %d", &a, &b);
		if (find_set(arr[a]) != find_set(arr[b]))
		{
			//printf("%d, %d", find_set(arr[a]), find_set(arr[b]));
			union_set(arr[a], arr[b]);
			ret--;
		}
	}
	//for (int i = 1; i <= n; ++i)printf("%d %d\n", i, arr[i]->presenter);
	printf("%d", ret);
}