def check_number(num):
    if num > 0:
        return "Positive"
    elif num < 0:
        return "Negative"
    else:
        return "Zero"


for i in range(-3, 4):
    print(str(i) + " is " + check_number(i))
