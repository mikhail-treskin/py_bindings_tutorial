To build C library
```shell script
cd <repo_root>/c_library
mkdir build
cd build
cmake .. && make
```


To build cython modules
``` shell script
python3 build.py build_ext --inplace 
```

To run cython modes vs extern C implementation
``` shell script
python3 perf_demo.py
```
