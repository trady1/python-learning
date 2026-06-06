person = name = {
    "name": "Aron",
    "age": 22,
    "city": "Budapest"
}

print(person["name"])
print(person["age"])
print(person["city"])
person["job"] = "Developer"
print(person)
for key, value in person.items():
    print(key + ": " + str(value))
