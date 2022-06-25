#include <stdio.h>
#include <stdlib.h>


void show_arr(int* arr, int start_index, int end_index)
{
	for (int i = start_index;  i <= end_index; i++)
	{
		printf("%d\n", arr[i]);
	}
}
void move_back(int* arr, int index, int end)  //한칸씩 뒤로
{
	int temp;
	for (int i = end; i > index; i--)
	{
		arr[i] = arr[i - 1];
	}

}
int main()
{
	int n;
	int* arr;
	int temp;
	scanf("%d", &n);
	arr = (int*)malloc(sizeof(int) * (n+1));
	arr[0] = 987654321;   //첫번쨰 값을 무한대로 시작=1,끝=n

	for (int i = 1; i<=n; i ++)
	{
		scanf("%d", &arr[i]);
	}

	for (int i = 1; i<=n ;i++)
	{
		for (int j = 1; j<i; j++)  //j는 i보다 앞에있는 배열변수
		{
			if (arr[i] > arr[j])
			{
				temp = arr[i];
				move_back(arr, j, i);
				arr[j] = temp;
				break;
			}
		}
	}

	show_arr(arr, 1, n);
	return 0;
}