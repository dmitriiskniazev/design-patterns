from baseline.client import Format, validate_and_read, write_and_read

if __name__ == "__main__":
    data = {"message": "hello"}
    for format in Format:
        print(write_and_read(format, data))
    print(validate_and_read(Format.JSON, '{"message": "hello"}'))
