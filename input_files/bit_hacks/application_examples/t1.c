#include<stdio.h>
#include<string.h>

int hasUniqueChars(char *str){
    /*unique-characters-begin*/
    int n = strlen(str);
    for (int i = 0; i < n ; i++) {
        for (int j = i + 1; j < n; j++) {
            if (str[i] == str[j]) {
                return 0;
            }
        }
    }
    return 1;
    /*unique-characters-end*/
}

int main() {
    char str[100];
    printf("Enter string (lowercase alphabets only): ");
    scanf("%s", str);
    int r = hasUniqueChars(str);
    if(r==1)
    {
        printf("Unique\n");
    }
    else{
        printf("Not unique\n");
    }
    return 0;
}