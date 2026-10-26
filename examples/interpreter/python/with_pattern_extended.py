from expression import Literal, Sum

if __name__ == "__main__":
    print(Sum(Literal(1), Literal(2)).evaluate())
