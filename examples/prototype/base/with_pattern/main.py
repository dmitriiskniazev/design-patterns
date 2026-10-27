from prototype import Prototype

if __name__ == "__main__":
    original = Prototype(["A"])
    print(original.clone().parts)
