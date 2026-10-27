from prototype import Prototype

if __name__ == "__main__":
    original = Prototype(["A"])
    clone = original.clone()
    clone.parts.append("B")
    print(clone.parts)
