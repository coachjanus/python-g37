# Функції вищого порядку приймають одну або кілька функцій в якості аргументів  або повертають одну або кілька функцій.
def outer(): # outer() визначає локальну функцію inner().
  def inner():
        print("I am function inner()!")
  return inner   # Function outer() returns function inner()

function = outer() # значення, що повертається з outer(), призначається змінній.
print(function) # <function outer.<locals>.inner at 0x7f18bc85faf0>
# Після цього можна викликати inner()
function() # I am function inner()!
# Можна навіть не застосовувати проміжного function
outer()() # I am function inner()!

