from component import Composite, Leaf, RepeatedComponent

if __name__ == "__main__":
    print(Composite([Leaf(1), RepeatedComponent(Composite([Leaf(2)]))]).operation())
