#include "stdio.h"
#include "stdlib.h"

typedef struct stackLink {
    int data;
    struct stackLink *next;
} StackLink;

// 数据弹出栈
int pop(StackLink *top){
    int data;
    if (top->next) {
        data = top->next->data;
        top->next = top->next->next;
    } else {
        // 空栈
        printf("empty stack");
        data = -1;
    }
    return data;
}

//数据压入栈
void push(StackLink *top, int data){
    StackLink* new = malloc(sizeof(StackLink));
    new->data = data;
    new->next = NULL;
    if (top->next) new->next = top->next;
    //栈顶指向新节点
    top->next = new;
}

// 栈是否为空
int isEmpty(StackLink *top) {
    return top->next ? 0 : 1;
}

// 10进制转2进制
void dec2bin(int number) {
    if (number < 0) {
        puts("只给转大于0的");
        return;
    }
    // 初始化栈列表
    StackLink* stack = malloc(sizeof(StackLink));
    stack->next = NULL;
    while (number) push(stack, number%2), number /= 2;
    // 输出结果
    printf("结果为：");
    while(!isEmpty(stack)) printf("%d", pop(stack));
    puts("");
}

int main(int argc, char const *argv[]) {
    int number;
    printf("请输入转进制的数：");
    scanf("%d", &number);
    dec2bin(number);
    return 0;
}
