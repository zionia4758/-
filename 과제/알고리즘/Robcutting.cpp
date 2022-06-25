#include<stdio.h>


int rob[101] = { 0 };
int value[101] = { 0 };
int cut[101] = { 0 };
int max(int a, int b)
{
	if (a >= b)return a;
	else return b;
}
int rob_cutting(int leng)
{
	if (value[leng] != 0) return value[leng];
	if (leng == 0) return 0;
	int ret = -123456789;
	for (int i = 1; i <= leng; ++i)
	{
		int a = rob[i] + rob_cutting(leng - i);
		if (a > ret)
		{
			cut[leng] = i;
			ret = a;
		}
	}
	value[leng] = ret;
	return ret;
}

int main()
{
	int n;
	scanf("%d", &n);
	for (int i = 1; i <= n; ++i)
	{
		scanf("%d", rob + i);
	}
	printf("%d\n", rob_cutting(n));
	int p = n;
	while (cut[p] > 0)
	{
		printf("%d ", cut[p]);
		p = p - cut[p];
	}

	return 0;
}