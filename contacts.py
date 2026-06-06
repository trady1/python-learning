person = {
    "name": "Aron",
    "phone": "123-456-7890",
    "email": "aron@example.com"
}

print("Name: " + person["name"])
print("Phone: " + person["phone"])
print("Email: " + person["email"])

for key, value in person.items():
    print(key + ": " + value)
