build:
	g++ -c -fpic CppForPython.cpp -o CppForPython.o
	g++ -shared -static -Wl,-soname,CppForPython.so -o CppForPython.so CppForPython.o

clean:
	rm *.so