from builder import Builder

if __name__ == "__main__":
    builder = Builder()
    builder.add("A")
    builder.add("B")
    print(builder.build().parts)
