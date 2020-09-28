"""Example of call C++ function from a python file."""
import ctypes

lib = ctypes.CDLL("./CppForPython.so")

if __name__ == "__main__":
    print("Printing from python")
    lib.HelloWorld()
