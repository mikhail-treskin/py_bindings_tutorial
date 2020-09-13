#include "library.h"

#include <stdio.h>
#include <string.h>
#include <unistd.h>
#include <stdlib.h>

void arr_minus_one(void *data, unsigned int arr_size, unsigned int el_size, char *el_type) {
    printf("From C Library:\n");
    for (int i = 0; i < arr_size; ++i) {
        if (strcmp(el_type, "int32") == 0) {
            printf("%d ", *(int *) (data + i * el_size) - 1);
        } else if (strcmp(el_type, "float") == 0) {
            printf("%f ", *(float *) (data + i * el_size) - 1.);
        }
    }
    printf("\n");
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