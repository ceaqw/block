#include <stdio.h>

// 最长数据位数
#define MAX_LENGTH 10000

void calcBigNumberFactorial(unsigned int number) {
    // 初始化抽象结果储存数组
    int result_abstract_list[MAX_LENGTH] = {0};
    int i, j, carryNumber, nextLen = 1;
    result_abstract_list[0] = 1;

    for (i = 1; i <= number; i++) {
        carryNumber = 0;
		for(j=0; j < nextLen; j++) {
			result_abstract_list[j] = result_abstract_list[j]*i+carryNumber;
            //处理进位
			if (result_abstract_list[j] >= 10) {
				carryNumber = result_abstract_list[j]/10;
				result_abstract_list[j] = result_abstract_list[j]%10;
			} else {
				carryNumber = 0;
			}
		}
        //最高位仍然有进位
		while (carryNumber > 0) {
			result_abstract_list[nextLen] = carryNumber%10;
			carryNumber = carryNumber/10;
			nextLen ++;
            if (nextLen >= MAX_LENGTH) {
                puts("数据超界");
                return;
            }
		}
    }

    printf("结果为：");
    for(i = nextLen-1; i >= 0; i--) {
		printf("%d",result_abstract_list[i]);
	}
	printf("\n");   
}

void calcFactorial(int number) {
    if (number < 1) {
        printf("结果为：0\n");
        return;
    }
    int i, result = 1;
    for (i = 1; i <= number; i++) {
        result *= i; 
    }
    printf("结果为：%d\n", result);
}

int main(int argc, char const *argv[]) {
    int number;
    printf("请输入计算阶乘数：");
    scanf("%d", &number);
    if (number < 13) calcFactorial(number);
    else calcBigNumberFactorial(number);
    return 0;
}
