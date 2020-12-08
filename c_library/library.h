/*
CDefError: cannot parse "#include <stdio.h>"
<cdef source string>:1:1: Directives not supported yet

CFFI doesn't support directives in headers
For compatibility between ctypes and CFFI all includes moved to .c files
#include <stdio.h>
#include <string.h>
#include <unistd.h>
*/

int func_ret_int(int val);
double func_ret_double(double val);
char *func_ret_str(char *val);
char func_many_args(int val1, double val2, char val3, short val4);

void arr_minus_one(int *data, unsigned int arr_size);
int *gen_arr(unsigned int size);
void fill_arr(int *arr, unsigned int size);
void qsort_wrap(int *arr, unsigned int size, unsigned int el_size);
int comp (const int *a, const int *b);
void upd_arr(int *arr, unsigned int size, int(*callback)(int));
void free_arr(int *p);

char *do_nothing_function(char *some_str);