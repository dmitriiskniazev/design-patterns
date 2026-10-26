from command import Increment
from invoker import Invoker
from receiver import Receiver

if __name__ == "__main__":
    receiver = Receiver(2)
    Invoker().run(Increment(receiver))
    print(receiver.value)
