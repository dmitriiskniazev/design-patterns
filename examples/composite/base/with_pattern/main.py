from component import Composite, Leaf

if __name__ == "__main__":
    print(Composite([Leaf(1), Composite([Leaf(2)])]).operation())
