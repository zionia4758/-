#include <stdio.h>
#include <stdlib.h>
//2016025196_김동규_알고리즘문제해결기법

void Max_heap_sort(int*arr,int i,int& index)
{

	int right = i * 2 + 1;
	int left = i * 2;
	int largest = i;
	int temp;

	if (left <= index && arr[i] < arr[left])
		largest = left;
	if (right <= index && arr[largest] < arr[right])
		largest = right;
	if (i == largest)
		return;

	temp = arr[largest];
	arr[largest] = arr[i];
	arr[i] = temp;
	Max_heap_sort(arr,largest,index);
	return;

}

void Insert_heap(int* arr,int& index,int num)
{
	if (index == 100001)
		return;
	arr[++index] = num;
	for (int i = index; i > 0; i /= 2)
		Max_heap_sort(arr,i,index);
	//just_show();
	return;

}
int Delete_queue(int*arr,int& index)
{
	int result = arr[1];
	if (index == 0) return -1111;
	arr[1] = arr[index];
	index--;
	Max_heap_sort(arr,1,index);
	//just_show();
	return result;
}
int main()
{
	int n, m;
	int* n_arr, * m_arr;
	int n_index = 0, m_index = 0;
	int cnt = 0;
	int num;
	scanf("%d %d", &n, &m);
	n_arr = (int*)malloc(sizeof(int) * (n+1));
	m_arr = (int*)malloc(sizeof(int) * (m+1));
	
	for (int i = 1; i <= n; ++i)
	{
		scanf("%d", & num);
		Insert_heap(n_arr, n_index, num);
	}
	for (int i = 1; i <= m; ++i)
	{
		scanf("%d", &num);
		Insert_heap(m_arr, m_index, num);
	}

	

	/*for (int i = 1; i <= n; ++i)
		printf("%d ", n_arr[i]);
	printf("\n");
	for (int i = 1; i <= m; ++i)
		printf("%d ", m_arr[i]);
	printf("\n");*/
	int a, b;
	a = Delete_queue(n_arr, n_index);
	b = Delete_queue(m_arr, m_index);
	for (int i = 0,  j = 0; i < n && j < m;)
	{

		if (a == b)
		{
			i++;
			j++;
			cnt++;
			a = Delete_queue(n_arr, n_index);
			b = Delete_queue(m_arr, m_index);
			continue;
		}
		else if (a > b)
		{
			a = Delete_queue(n_arr, n_index);
			i++;
			continue;
		}
		else
		{
			b = Delete_queue(m_arr, m_index);
			j++;
			continue;
		}
	}
	printf("%d",cnt);

	return 0;
}