#include "library.h"

#include <stdio.h>
#include <string.h>
#include <unistd.h>
#include <stdlib.h>

void arr_minus_one(int *data, unsigned int arr_size) {
    printf("From C Library:\n");
    for (int i = 0; i < arr_size; ++i) {
        data[i] = data[i] - 1;
        printf("%d ", data[i]);
    }
}

int *gen_static_arr() {
    static int arr[10];
    for (int i = 0; i < 10; ++i) {
        arr[i] = i;
    }
    return arr;
}

void gen_arr(int *arr, unsigned int size) {
    for (int i = 0; i < size; ++i) {
        arr[i] = i;
    }
}

void qsort_wrap(int *arr, unsigned int size, unsigned int el_size) {
    qsort(arr, size, el_size, (int (*)(const void *, const void *)) comp);
}

int comp(const int *a, const int *b) {
    return *a - *b;
}