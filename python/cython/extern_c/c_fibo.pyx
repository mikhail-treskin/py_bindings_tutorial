cimport c_fibo

def extern_c_fibo(n):
    return c_fibo.fib(n)