from command import Double
from invoker import Invoker
from receiver import Receiver

if __name__ == "__main__":
    receiver = Receiver(2)
    Invoker().run(Double(receiver))
    print(receiver.value)
