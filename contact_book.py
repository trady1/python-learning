import json


def save_contacts(contacts):
    file = open("contacts.json", "w")
    json.dump(contacts, file)
    file.close()


def load_contacts():
    try:
        file = open("contacts.json", "r")
        contacts = json.load(file)
        file.close()
        return contacts
    except:
        return []


contacts = load_contacts()


def add_contact(name, phone):
    contact = {"name": name, "phone": phone}
    contacts.append(contact)
    save_contacts(contacts)
    print("Contact added!")


def show_contacts():
    for contact in contacts:
        print(contact["name"] + " - " + contact["phone"])


def search_contact(name):
    for contact in contacts:
        if contact["name"] == name:
            print("Found: " + contact["name"] + " - " + contact["phone"])
            return
    print("Contact not found.")


while True:
    print("\n1. Add contact")
    print("2. Show contacts")
    print("3. Search contact")
    print("4. Quit")
    choice = input("Choose: ")

    if choice == "1":
        name = input("Name: ")
        phone = input("Phone: ")
        add_contact(name, phone)
    elif choice == "2":
        show_contacts()
    elif choice == "3":
        name = input("Search: ")
        search_contact(name)
    elif choice == "4":
        break
