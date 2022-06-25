#include <stdio.h>



int bitCount(int x)
{
	int cnt = 0;
	int bit01 = x &0x01010101;
	//printf("%08x\n", x);
	//printf("%08x\n", bit01);
	bit01 += (x >> 1) & 0x01010101;
	//printf("%08x\n", x>>1);
	//printf("%08x\n", bit01);
	bit01 += (x >> 2) & 0x01010101;
	//printf("%08x\n", x>>2); printf("%08x\n", bit01);
	bit01 += (x >> 3) & 0x01010101;
	//printf("%08x\n", x>>3); printf("%08x\n", bit01);
	bit01 += (x >> 4) & 0x01010101;
	//printf("%08x\n", x>>4); printf("%08x\n", bit01);
	bit01 += (x >> 5) & 0x01010101;
	//printf("%08x\n", x>>5); printf("%08x\n", bit01);
	bit01 += (x >> 6) & 0x01010101;
	//printf("%08x\n", x>>6); printf("%08x\n", bit01);
	bit01 += (x >> 7) & 0x01010101;
	//printf("%08x\n", x>>7); printf("%08x\n", bit01);
	cnt += (int)(bit01) & 0xff;
	cnt += (int)(bit01 >> 8) & 0xff;
	cnt += (int)(bit01 >> 16) & 0xff;
	cnt +=(int) (bit01 >> 24) & 0xff;
	//printf("%08x , %08x, %08x", bit01>>32 , 0xff,(int) (bit01>>32) & 0xff);
	//printf("%08x\n", bit01>> 32);
	return cnt;

}
int bitMask(int highbit, int lowbit) {
	int mask = ~0;
	
	int highmask = mask << lowbit;
	printf("%08x\n", mask);
	int lowmask = ((~((1 << 31) >> highbit)) << 1) + 1;
	printf("mask::: %08x, %08x\n", highmask, lowmask);
	return highmask & lowmask;

}
int byteSwap(int x, int n, int m) {
	int nbyte = 0xff << (n << 3);
	int mbyte = 0xff << (m << 3);
	int ntombyte = ((x & nbyte) >> nbyte) & 0xff;
	int mtonbyte = ((x & mbyte) >> mbyte) & 0xff;
	x = x & (~nbyte) & (~mbyte);
	x = x | (ntombyte << (m << 3)) | (mtonbyte << (n << 3));
	printf("%08x %08x\n", ntombyte, mtonbyte);
	/*
	int n_byte_mask=0xff<<(n<<3);
	int m_byte_mask=0xff<<(m<<3);
	int n_byte=(x&n_byte_mask)>>(n<<3);
	int m_byte=(x&m_byte_mask)>>(m<<3);

	x=(x&(~n_byte_mask))&(~m_byte_mask);
	n_byte=n_byte<<(m<<3);
	m_byte=m_byte>>(n<<3);
	x=x|n_byte|m_byte;
	*/
	return x;
}
int conditional(int x, int y, int z)
{
	int mask = ((!x - 1) >> 31);
	return (mask & y) | (~mask & z);
}
int logicalShift(int x, int n) {
	int zeromask = (!n +~1+1);
	x = x >> n;
	x = x & ~((~0 << (33 + ~n)) & zeromask);
	return x;
}



int DDiyong(int highbit)
{
	int mask = ~0;
	int i = 31;
	printf("\n%08x\n",mask);
	int result = (mask<<highbit);
	printf("\n%08x\n", result);
	return result;

}

int main()
{
	struct { int a; int b; }*str;
	printf("%d", sizeof(str));
	str = malloc(sizeof(str));


}