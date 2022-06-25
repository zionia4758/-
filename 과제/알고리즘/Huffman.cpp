//2016025196_김동규_알고리즘문제해결기법

#include <stdio.h>	
#include <stdlib.h>

static int index = 0;
static int n;
static int arr[30001] = { 0 };

void Min_heap_sort(int i)
{

	int right = i * 2 + 1;
	int left = i * 2;
	int largest = i;
	int temp;

	if (left <= index && arr[i] > arr[left])
		largest = left;
	if (right <= index && arr[largest] >= arr[right])
		largest = right;
	if (i == largest)
		return;

	temp = arr[largest];
	arr[largest] = arr[i];
	arr[i] = temp;
	Min_heap_sort(largest);
	return;

}
void just_show()
{
	printf("\n");
	for (int i = 1; i <= index; ++i)
		printf("%d ", arr[i]);
	//printf("\n");
	return;
}
void Insert_heap(int num)
{
	if (index == 100001)
		return;
	arr[++index] = num;
	for (int i = index; i > 0; i /= 2)
		Min_heap_sort(i);
	//just_show();
	return;

}

int Delete_queue()
{
	int result = arr[1];
	if (index == 0) return result;
	arr[1] = arr[index];
	index--;
	Min_heap_sort(1);
	//just_show();
	return result;
}

int main()
{

	int total;
	int k = 0;
	int num;
	int ret = 0;

	scanf("%d", &n);
	for (int i = 0; i < n; ++i)
	{
		char str[5];
		scanf("%s %d", str,&num);
		Insert_heap(num);
	}
	for (int i = 0; i < n - 1; ++i)
	{
		int a = Delete_queue();
		int b = Delete_queue();
		ret += (a + b);
		Insert_heap(a + b);
	}
	scanf("%d", &total);
	for (int i = n-1; i > 0; i /= 2)
	{
		k++;
	}
	//fixed length
	printf("%d\n", total * k);
	printf("%d\n", ret);
	return 0;
}