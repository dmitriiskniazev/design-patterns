from nodes import A, B
from visitor import DoubleVisitor

if __name__ == "__main__":
    print(B(A(2)).accept(DoubleVisitor()))
