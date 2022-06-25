//2016025196_김동규_알ㄹ고리즘문제해결기법

#include <stdio.h>
int p[101] = { 0 };
int m[2][101][101] = { 0 };

int min(int a, int b)
{
	if (a <= b)
		return a;
	else
		return b;


}
/*
void matrix(int n)
{
	for (int z = 1; z < n; ++z)
	{
		
		for (int x = 0; x < z; ++x)
		{
			int ret = 98654321;

			for (int k = x; k < z; ++k)
			{
				
				if (ret > m[x][k] + m[k + 1][z] + p[x] * p[k + 1] * p[z + 1])
				{
					ret = m[x][k] + m[k + 1][z] + p[x] * p[k + 1] * p[z + 1];
					printf("x: %d z: %d k: %d    %d, %d \n",x,z,k,ret, p[x] * p[k + 1] * p[z + 1]);
				}

			}
			m[x][z] = ret;
			
		}
	}
}
void show(int n,int s,int k)
{
	if (k == 0)
	{
		//printf("(%d %d)", s, n);
		for (int i = 0; i < n-s; ++i)
		{
			printf("(%d ", s + i);
		} 
		printf("%d", n);
		for (int i = 0; i < n-s; ++i)
			printf(")");
		return;


	}
	
	show(k,s ,m[1][0][k]);

	show(n,k+1, m[1][k + 1][n]);
	

}*/

void show( int i, int j)
{
	if (i == j)
		printf("%d ", i);
	else
	{
		printf("( ");
		show(i, m[1][i][j]);
		show(m[1][i][j] + 1, j);
		printf(") ");
	}
}
void matrix(int n)
{
	int z_z;
	for (int z = 1; z < n; ++z)
	{

		for (int x = 0, z_z = z; z_z < n; ++x, ++z_z)
		{
			int ret = 98654321;

			for (int k = x; k < z_z; ++k)
			{


				if (ret > m[0][x][k] + m[0][k + 1][z_z] + p[x] * p[k + 1] * p[z_z + 1])
				{
					ret = m[0][x][k] + m[0][k + 1][z_z] + p[x] * p[k + 1] * p[z_z + 1];
					//	printf("x: %d z_z: %d k: %d   %d %d, %d \n", x, z_z, k, m[x][k] + m[k + 1][z_z], ret, p[x] * p[k + 1] * p[z_z + 1]);
					m[1][x][z_z] = k;
				}

			}
			m[0][x][z_z] = ret;

		}
	}

}

int main()
{
	int n;
	scanf("%d", &n);
	for (int i = 0; i <= n; ++i)
	{
		scanf("%d", p + i);
	}
	for (int i = 0; i < n-1; ++i)
	{
		m[0][i][i + 1] = p[i] * p[i + 1] * p[i + 2];
	}


	matrix(n);


	printf("%d\n", m[0][0][n-1]);
	show(0, n - 1);
/*
	for (int i = 0; i < n; ++i)
	{
		printf("%d : ", i);
		for (int a = 0; a < i; ++a) printf("%10d", 0);
		for (int j = i; j < n; ++j)
		{
			printf("%10d", m[i][j]);
		}
		printf("\n");
	}
	*/
	
	return 0;
}