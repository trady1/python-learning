try:
    number = int(input("Enter a number: "))
    print(10 / number)
except ZeroDivisionError:
    print("You cannot divide by zero!")
except ValueError:
    print("That is not a number!")
