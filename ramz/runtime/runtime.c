#include <stdio.h>

void print_int(int x) {
    printf("%d\n", x);
}

void print_boolean(int x) {
    printf("%s\n", x ? "True" : "False");
}

void print_decimal(double x) {
    printf("%f\n", x);
}

void print_string(char* x) {
    printf("%s\n", x);
}