try:
    number = int(input("Enter a number? "))
    print(f"You entered: {number}")
except ValueError:
    print("Invalid input. Please enter a valid integer.")
