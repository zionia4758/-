#include <stdio.h>
#include <stdlib.h>
//2016025196_김동규_알고리즘문제해결기법

static int n;
void Max_heap_sort(int* arr, int i)
{

	int right = i * 2 + 1;
	int left = i * 2;
	int largest = i;
	int temp;

	if (left <= n && arr[i] < arr[left])
		largest = left;
	if (right <= n && arr[largest] < arr[right])
		largest = right;
	if (i == largest)
		return;

	temp = arr[largest];
	arr[largest] = arr[i];
	arr[i] = temp;
	Max_heap_sort(arr, largest);
	return;

}


int main()
{
	int k;
	int* arr;
	int index;
	scanf("%d", &n);
	arr = (int*)malloc(sizeof(int) * (n + 1));
	scanf("%d", &k);

	for (int i = 1; i <= n; ++i)
	{
		scanf("%d", arr + i);
	}


	for (int i = n / 2; i >= 1; --i)
		Max_heap_sort(arr, i);
	/*

	for (int i = 0; i < n; ++i)
		printf("%d ", arr[i]);
	for (int i = 0; i < k-n; ++i)
		printf("%d ", arr[i]);
		*/

	for (index = 0; index < k; ++index)
	{
		printf("%d ", arr[1]);
		arr[1] = arr[n];
		n--;
		Max_heap_sort(arr, 1);
	}
	printf("\n");
	while (n > 0)
	{	//for (int i = 1; i <= n; ++i)
		//	printf("##%d ", arr[i]);
		//printf("\n\n");


		printf("%d ", arr[1]);

		arr[1] = arr[n];
		n--;
		if (n >= 0)
			Max_heap_sort(arr, 1);

	}


	return 0;
}