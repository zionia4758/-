#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void show_arr(int* arr, int start_index, int end_index)
{
	for (int i = start_index; i < end_index; i++)
	{
		printf("%d\n", arr[i]);
	}
}

void merge(int* arr1, int* arr2, int i, int j, int i_end, int j_end) //i=arr1,j=arr2
{
	int index = i;
	//printf("------%d~~%d\n\n", i, j_end-1);
	int temp_i = i;
	int temp_j_end = j_end;
	while (i < i_end || j < j_end)
	{
		//어느 한쪽이 경계에 닿으면 스킵
		if (i >= i_end)
		{
			while (j < j_end)
			{
				arr2[index++] = arr1[j++];
			}
		}
		else if (j >= j_end)
		{
			while (i < i_end)
				arr2[index++] = arr1[i++];
		}

		else {
			if (i == 32 && j == 34);
			if (arr1[i] > arr1[j])
			{
				arr2[index++] = arr1[i];
				i++;
			}
			else if (arr1[i] <= arr1[j])
			{
				arr2[index++] = arr1[j];
				j++;

			}
		}
	}
	//show_arr(arr2, temp_i, temp_j_end);
	//printf("\n");

}



int main()
{
	int n;
	int* arr1, * arr2;
	scanf("%d", &n);

	arr1 = (int*)malloc(sizeof(int) * n);
	arr2 = (int*)malloc(sizeof(int) * n);


	for (int i = 0; i < n; ++i)
	{
		scanf("%d", &arr1[i]);
	}
	for (int i = 0; i < n; ++i)
	{
		arr2[i] = arr1[i];
	}
	for (int range = 1; range < n; range *= 2)
	{
		int flag = 0;
		for (flag = 0; flag + (2 * range) <= n; flag += 2 * range)
			merge(arr1, arr2, flag, flag + range, flag + range, flag + (2 * range));

		//2range보다 작게range보다 크게 남은 부분 merge 
		if (flag + range < n)
			merge(arr1, arr2, flag, flag + range, flag + range, n);


		for (int i = 0; i < n; ++i)
		{
			arr1[i] = arr2[i];
		}
		//show_arr(arr1, 0, n);
	//	printf("\n");
	}
	free(arr2);
	show_arr(arr1, 0, n);
	free(arr1);
	return 0;
}v#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void show_arr(int* arr, int start_index, int end_index)
{
	for (int i = start_index; i < end_index; i++)
	{
		printf("%d\n", arr[i]);
	}
}

void merge(int* arr1, int* arr2, int i, int j, int i_end, int j_end) //i=arr1,j=arr2
{
	int index = i;
	//printf("------%d~~%d\n\n", i, j_end-1);
	int temp_i = i;
	int temp_j_end = j_end;
	while (i < i_end || j < j_end)
	{
		//어느 한쪽이 경계에 닿으면 스킵
		if (i >= i_end)
		{
			while (j < j_end)
			{
				arr2[index++] = arr1[j++];
			}
		}
		else if (j >= j_end)
		{
			while (i < i_end)
				arr2[index++] = arr1[i++];
		}

		else {
			if (i == 32 && j == 34);
			if (arr1[i] > arr1[j])
			{
				arr2[index++] = arr1[i];
				i++;
			}
			else if (arr1[i] <= arr1[j])
			{
				arr2[index++] = arr1[j];
				j++;

			}
		}
	}
	//show_arr(arr2, temp_i, temp_j_end);
	//printf("\n");

}



int main()
{
	int n;
	int* arr1, * arr2;
	scanf("%d", &n);

	arr1 = (int*)malloc(sizeof(int) * n);
	arr2 = (int*)malloc(sizeof(int) * n);


	for (int i = 0; i < n; ++i)
	{
		scanf("%d", &arr1[i]);
	}
	for (int i = 0; i < n; ++i)
	{
		arr2[i] = arr1[i];
	}
	for (int range = 1; range < n; range *= 2)
	{
		int flag = 0;
		for (flag = 0; flag + (2 * range) <= n; flag += 2 * range)
			merge(arr1, arr2, flag, flag + range, flag + range, flag + (2 * range));

		//2range보다 작게range보다 크게 남은 부분 merge 
		if (flag + range < n)
			merge(arr1, arr2, flag, flag + range, flag + range, n);


		for (int i = 0; i < n; ++i)
		{
			arr1[i] = arr2[i];
		}
		//show_arr(arr1, 0, n);
	//	printf("\n");
	}
	free(arr2);
	show_arr(arr1, 0, n);
	free(arr1);
	return 0;
}