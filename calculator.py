num1 = input("Enter first number: ")
num2 = input("Enter second number: ")

print("The sum of " + num1 + " and " + num2 +
      " is " + str(int(num1) + int(num2)))
print("The difference of " + num1 + " and " +
      num2 + " is " + str(int(num1) - int(num2)))
print("The product of " + num1 + " and " +
      num2 + " is " + str(int(num1) * int(num2)))
if int(num2) == 0:
    print("Cannot divide by zero")
else:
    print("The division of " + num1 + " and " +
          num2 + " is " + str(int(num1) / int(num2)))
