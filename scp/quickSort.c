#include "stdio.h"
#include "stdlib.h"
#include "time.h"
#define MAX_LENGTH 10000

int randNumbers[MAX_LENGTH] = {0};

void show(const char* title) {
    puts(title);
    int i;
    for (i = 0; i < MAX_LENGTH; i++) printf("%d ", randNumbers[i]);
    puts("");
}

void initRandNumber() {
    int i;
    srand(time(0));
    for (i = 0; i < MAX_LENGTH; i++) randNumbers[i] = rand()%(MAX_LENGTH+1);
}

// 快速排序
void quickSort(int left, int right) {
    if (left < right) {
        int i = left, j = right, mid = randNumbers[left];
        // 循环一次，小的放一边，大的放一边
        while (i < j) {
            // 从右向左找第一个小于mid的数
            while(i < j && randNumbers[j] >= mid) j--;
            if(i < j) randNumbers[i++] = randNumbers[j];

            // 从左向右找第一个大于等于mid的数
            while(i < j && randNumbers[i] < mid) i++;
            if(i < j) randNumbers[j--] = randNumbers[i];
        }
        randNumbers[i] = mid;
        // 递归调用
        quickSort(left, i-1);     // 排序mid左边
        quickSort(i+1, right);    // 排序mid右边
    }
}

int main(int argc, char const *argv[]) {
    initRandNumber();
    show("排序前结果为：");
    quickSort(0, MAX_LENGTH-1);
    show("快速排序后结果为：");
    return 0;
}
