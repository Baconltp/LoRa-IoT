#include<reg51.h>
#include<intrins.h>
#define uchar unsigned char
#define uint unsigned int

uchar tab1[]={0x33,0x96,0xcc,0x69};
uchar tab2[]={0x33,0x69,0xcc,0x96};
#define motor P0
uchar i,j;
uchar s;
void delay(uchar ms){
    uchar j;
    while(ms--){
        for(j=0;j<250;j++)
            {;}
    }
}
bit stat = 1;
void main(){
    EA=1;
    EX0=1;
	EX1=1;
    while(1){
        j=0;
		if(stat == 0)
			continue;
		if(s == 1){
			for(i=0;i<64;i++){
				motor = 0x00;
				motor = tab1[j];
				j++;
				if(j>=4)
					j=0;
				delay(1);
			}
		}
		if(s == 0){
			for(i=0;i<64;i++){
				motor = 0x00;
				motor = tab2[j];
				j++;
				if(j>=4)
					j=0;
				delay(1);
			}
		}
    }
}

void int0() interrupt 0
{
    stat=~stat;
	delay(500);
}

void int1() interrupt 2
{
	s++;
	s=s%2;
	delay(500);
}