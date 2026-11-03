from pattern.client import validate_and_read, write_and_read
from pattern.factories import JsonFactory, TomlFactory, YamlFactory

if __name__ == "__main__":
    data = {"message": "hello"}
    for factory in (JsonFactory(), YamlFactory(), TomlFactory()):
        print(write_and_read(factory, data))
    print(validate_and_read(JsonFactory(), '{"message": "hello"}'))
