#include<stdio.h>
#include<stdlib.h>
//2016025196_김동규_알고리즘문제해결
int main()
{
	int n;
	int m;
	int k;
	int index;
	scanf("%d %d %d", &n, &m, &k);
	int* m_arr = (int*)malloc(sizeof(int) * (m+1));
	int* k_arr_a = (int*)malloc(sizeof(int) * k);
	int* k_arr_b = (int*)malloc(sizeof(int) * k);
	for (int i = 0; i < m + 1; ++i)
		m_arr[i] = 0;
	for (int i = 0; i < k; ++i)
	{
		scanf("%d %d", &k_arr_a[i], &k_arr_b[i]);
	}
	for(int i=0;i<n;++i)
	{
		scanf("%d", &index);
		m_arr[index]++;
	}
	for (int i = 1; i < m + 1; ++i)
		m_arr[i] += m_arr[i - 1];
	
	for (int i = 0; i < k; ++i)
		printf("%d\n", m_arr[k_arr_b[i]] - m_arr[k_arr_a[i]-1]);

	return 0;
}