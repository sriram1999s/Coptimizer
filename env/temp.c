#include<stdio.h>
int check_overlap(int x1, int y1, int x2, int y2) {if(x1>y1 || x2>y2)return 0;if((x1>=x2 && x1<y2) || (y1>x2 && y1<=y2) || ((x1<y1?x1:y1) > (x2<y2?x2:y2) && (x1>y1?x1:y1) < (x2>y2?x2:y2)) ||((x1<y1?x1:y1) < (x2<y2?x2:y2) && (x1>y1?x1:y1) > (x2>y2?x2:y2)))return 1;return 0;}int main(){int var1,var2,var3;scanf("%d",&var1);scanf("%d",&var2);scanf("%d",&var3);switch(var1) { case 0:{printf("var1 is 0");}break;case 1:{printf("var1 is 1");}break;case 2:{printf("var1 is 2");}break;case 3:{printf("var1 is 3");}break;case 4:{printf("var1 is 4");}break;case 5:{printf("var1 is 5");}break;case 6:{printf("var1 is 6");}break;case 7:{printf("var1 is 7");}break;case 8:{printf("var1 is 8");}break;case 9:{printf("var1 is 9");}break;case 10:{printf("var1 is 10");}break;case 11:{printf("var1 is 11");}break;case 12:{printf("var1 is 12");}break;case 13:{printf("var1 is 13");}break;case 14:{printf("var1 is 14");}break;case 15:{printf("var1 is 15");switch(var2) { case 0:if(var3<10){printf("var2 is 0, var3 is less than 10");}break;case 1:if(var3>=10&&var3<20){printf("var2 is 1, var3 is between 9 and 20");}break;case 2:if(var3>=10&&var3<20){printf("var2 is 2, var3 is between 9 and 20");}break;case 3:if(var3<10){printf("var2 is 3, var3 is less than 10");}break;case 4:if(var3<10){printf("var2 is 4, var3 is less than 10");}break;case 5:if(var3>=10&&var3<20){printf("var2 is 5, var3 is between 9 and 20");}break;case 6:{printf("var2 is 6");}break;case 7:{printf("var2 is 7");}break;case 8:{printf("var2 is 8");}break;case 9:{printf("var2 is 9");}break;case 10:{printf("var2 is 10");}break;case 11:{printf("var2 is 11");}break;case 12:{printf("var2 is 12");}break;case 13:{printf("var2 is 13");}break;case 14:{printf("var2 is 14");}break;case 15:{printf("var2 is 15");}break;case 16:{printf("var2 is 16");}break;case 17:{printf("var2 is 17");}break;case 18:{printf("var2 is 18");}break;case 19:{printf("var2 is 19");}break;case 20:{printf("var2 is 20");int i=0;while(i<10){if (var3==10){printf("var3 is 10");}else if (var3==20||var3==30){printf("var3 is 20 or 30");}else if (var3==40){printf("var3 is 40");}else if (var3==50){printf("var3 is 50");}else {printf("var3 other");}printf("chain 2 in while\n");switch(var3) { case 10:{printf("var3 is 10");}break;case 20:{printf("var3 is 20");}break;case 40:{printf("var3 is 40");}break;case 50:{printf("var3 is 50");}break;default: {printf("var3 other");}break;}i++;}}break;}}break;default: {printf("other");}break;}}