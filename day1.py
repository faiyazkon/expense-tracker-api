from abc import ABC, abstractmethod

class PaymentMethod(ABC):
    @abstractmethod
    def pay(self, amount):
        pass

class Bkash(PaymentMethod):
    def pay(self, amount):
        return f"Paid {amount} via bKash"

class Nagad(PaymentMethod):
    def pay(self, amount):
        return f"Paid {amount} via Nagad"

class CreditCard(PaymentMethod):
    def pay(self, amount):
        return f"Paid {amount} via Credit Card"


def checkout(payment_method, amount):
    print(payment_method.pay(amount))


# same function, 3 different behaviors
checkout(Bkash(), 500)
checkout(Nagad(), 500)
checkout(CreditCard(), 500)

# or loop through a list
methods = [Bkash(), Nagad(), CreditCard()]
for m in methods:
    print(m.pay(1000))