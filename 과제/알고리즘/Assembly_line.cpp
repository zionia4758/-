//2016025196_김동규_알고리즘문제해결기법

#include<stdio.h>

int arr[2][101] = { 0 };
int cross[2][100] = { 0 };
int val[2][100] = { 0 };
int route[2][100] = { 0 };
int x1, x2;
int l;
int s;

void print(int n,int r)
{
	if (n <= 0)return;

	print(n - 1, route[r-1][n - 1]);

	printf("%d %d\n", r, n);

}

void fastest(int n)
{
	int a, b;
	val[0][0] = arr[0][0] + arr[0][1];
	val[1][0] = arr[1][0] + arr[1][1];
	route[0][0] = 1;
	route[1][0] = 2;
	for (int i = 2; i <= n; ++i)
	{
		a = val[0][i - 2] + arr[0][i];
		b = val[1][i - 2] + arr[0][i] + cross[1][i - 2];
		if (a <= b)
		{
			val[0][i - 1] = a;
			route[0][i - 1] = 1;
		}
		else
		{
			val[0][i - 1] = b;
			route[0][i - 1] = 2;
		}


		a = val[1][i - 2] + arr[1][i];
		b = val[0][i - 2] + arr[1][i] + cross[0][i - 2];
		if (a <= b)
		{
			val[1][i - 1] = a;
			route[1][i - 1] = 2;
		}
		else
		{
			val[1][i - 1] = b;
			route[1][i - 1] = 1;
		}
	}
	if (val[0][n-1] + x1 <= val[1][n-1] + x2)
	{
		printf("%d\n", val[0][n-1] + x1);
		l = 1;
	}
	else
	{
		printf("%d\n", val[1][n-1] + x2);
		l = 2;
	}
	print(n,l);
}

int main()
{
	int n;

	int ret;
	scanf("%d", &n);
	scanf("%d %d", &arr[0][0],&arr[1][0]);
	scanf("%d %d", &x1, &x2);
	for (int i = 1; i <= n; ++i)
	{
		scanf("%d", arr[0] + i);
	}
	for (int i = 1; i <= n; ++i)
	{
		scanf("%d", arr[1] + i);
	}
	for (int i = 0; i < n-1; ++i)
	{
		scanf("%d", cross[0] + i);
	}
	for (int i = 0; i < n-1; ++i)
	{
		scanf("%d", cross[1] + i);
	}
	
	fastest(n);


	/*
	for (int i = 0; i <= n; ++i)printf("%d %d ab\n", arr[0][i], arr[1][i]);
	for (int i = 0; i < n-1; ++i) printf("%d %d cr\n", cross[0][i], cross[1][i]);
	for (int i = 0; i < n  ; ++i) printf("%d %d dd\n", val[0][i],val[1][i]);
	
	*/
	return 0;
}