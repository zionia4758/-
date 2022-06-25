#include <stdio.h>
#include <stdlib.h>
//2016025196_김동규_알고리즘문제해결기법

static int index=0;
int arr[100001] = { 0 };
void Max_heap_sort( int i)
{

	int right = i * 2 + 1;
	int left = i * 2;
	int largest = i;
	int temp;

	if (left <= index && arr[i] < arr[left])
		largest = left;
	if (right <= index && arr[largest] <= arr[right])
		largest = right;
	if (i == largest)
		return;

	temp = arr[largest];
	arr[largest] = arr[i];
	arr[i] = temp;
	Max_heap_sort( largest);
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
	for(int i=index;i>0;i/=2)
		Max_heap_sort(i);
	//just_show();
	return;

}

void Delete_queue()
{
	int result = arr[1];
	if (index == 0) return ;
	arr[1] = arr[index ];
	index--;
	Max_heap_sort(1);
	//just_show();
	printf("%d ", result);
	return ;
}
void Modify_queue(int target, int num)
{
	arr[target] = num;
	if (index < 2)
		return;
	/*if (arr[target] < arr[target *2]|| arr[target]<arr[target*2+1])
	{
		Max_heap_sort(target);
		//just_show();
		return;
	}*/
	while (arr[target] > arr[target / 2]&&target>1)
	{
		target /= 2;
		Max_heap_sort(target);
	}
	//just_show();
	Max_heap_sort(target);
	return;
}
void Show_heap()
{
	for (; index > 0; index--)
	{
		printf("%d ", arr[1]);
		arr[1] = arr[index];
		Max_heap_sort(1);
	}
	return;
}

void Select()
{
	int sel=99;
	int a, b;
	while (sel != 0)
	{
		scanf("%d", &sel);
		switch (sel)
		{
		case 0:
			just_show();
			break;

		case 1:
			scanf("%d", &a);
			Insert_heap( a);
			break;

		case 2:
			 Delete_queue();
			break;
			
		case 3:
			scanf("%d %d", &a, &b);
			Modify_queue(a,b);
			break;
		default:
			break;
		}
	}
}

int main()
{
	Select();




	return 0;
}