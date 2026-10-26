from builder import Builder

if __name__ == "__main__":
    builder = Builder()
    builder.add("A")
    print(builder.build().parts)
