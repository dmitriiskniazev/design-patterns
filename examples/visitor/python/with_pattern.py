from nodes import A, B
from visitor import ValueVisitor

if __name__ == "__main__":
    print(B(A(2)).accept(ValueVisitor()))
