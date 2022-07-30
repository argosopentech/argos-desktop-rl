from cffi import FFI
ffi = FFI()
ffi.set_source("_test", """
int key_pressed(int key) {
    return key;
}
""")
ffi.cdef("""int key_pressed(int);""")
ffi.compile()
from _test import lib
print(lib.key_pressed(42))

