#include "stdio.h"
#include "stdlib.h"
#include "time.h"
#define MAX_LENGTH 10000

int randAscNumbers[MAX_LENGTH] = {0};

void initRandNumber() {
    int i;
    srand(time(0));
    randAscNumbers[0] = rand()%11;
    for (i = 1; i < MAX_LENGTH; i++) randAscNumbers[i] = randAscNumbers[i-1] + rand()%11;
    printf("随机生成数据结果为：");
    for (i = 0; i < MAX_LENGTH; i++) printf("%d ", randAscNumbers[i]);
    puts("");
}

// 数据寻找(二分)
int binarySearch(int target, int left, int right, int *findCount) {
    int i, mid;
    mid = left + ((right-left)/2);
    // 查找次数+1
    (*findCount) ++;
    if (randAscNumbers[mid] == target) return mid;
    else if ((right-left) == 1) return randAscNumbers[mid+1] == target ? mid+1 : -1;
    else if ((right-left) < 1) return -1;
    else {
        // 继续拆分
        // 往右
        if (randAscNumbers[mid] < target) return binarySearch(target, mid, right, findCount);
        // 往左
        if (randAscNumbers[mid] > target) return binarySearch(target, left, mid, findCount);
    }
}

void findNumber(int number) {
    int result, findCount = 0;
    result = binarySearch(number, 0, MAX_LENGTH-1, &findCount);
    if (result != -1) printf("查找到该数据位置：%d, 查找次数：%d\n", result, findCount);
    else printf("未找到该数据, 查找次数：%d\n", findCount);
    system("pause");
}

int main(int argc, char const *argv[]) {
    initRandNumber();
    int cnt;
    while (1) {
        printf("请输入要查找的数：");
        scanf("%d", &cnt);
        findNumber(cnt);
        printf("是否退出查找(0.退出, 1.继续)：");
        scanf("%d", &cnt);
        if (!cnt) break;
    }
    return 0;
}
