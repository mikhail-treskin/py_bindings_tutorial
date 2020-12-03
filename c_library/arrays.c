#include "library.h"

#include <stdio.h>
#include <string.h>
#include <unistd.h>
#include <stdlib.h>

void arr_minus_one(int *data, unsigned int arr_size) {
    for (int i = 0; i < arr_size; ++i) {
        data[i] = data[i] - 1;
    }
}

int *gen_arr(unsigned int size) {
    int *arr = malloc(sizeof(int) * size);
    for (unsigned int i = 0; i < size; ++i) {
        arr[i] = i;
    }
    return arr;
}

void fill_arr(int *arr, unsigned int size) {
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