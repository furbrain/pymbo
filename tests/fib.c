#include <stdio.h>

int fib(int c) {
    switch (c) {
        case 0:
        case 1:
            return 1;
        default:
            return (fib(c-1) + fib(c-2));
    }
}

void main(char *argv[]) {
    printf("%d", fib(5));
}
