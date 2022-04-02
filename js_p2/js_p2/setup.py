from distutils.core import setup, Extension

def main():
    setup(name="simple_graphs",
          version="1.0.0",
          description="Python interface for the fputs C library function",
          author="zxx",
          author_email="your_email@gmail.com",
          ext_modules=[Extension("simple_graphs", ["simple_graphsmodule.c"])])

if __name__ == "__main__":
    main()