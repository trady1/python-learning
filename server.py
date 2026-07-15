from fastapi import FastAPI
import sqlite3

app = FastAPI()


def get_db():
    conn = sqlite3.connect("mydb.sqlite")
    conn.row_factory = sqlite3.Row
    return conn


def setup_db():
    conn = get_db()
    conn.execute(
        "CREATE TABLE IF NOT EXISTS contacts (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, phone TEXT NOT NULL)")
    conn.commit()
    conn.close()


setup_db()


@app.get("/contacts")
def get_contacts():
    conn = get_db()
    contacts = conn.execute("SELECT * FROM contacts").fetchall()
    conn.close()
    return {"contacts": [dict(c) for c in contacts]}


@app.get("/contacts/add/{name}/{phone}")
def add_contact(name: str, phone: str):
    conn = get_db()
    conn.execute(
        "INSERT INTO contacts (name, phone) VALUES (?, ?)", (name, phone))
    conn.commit()
    conn.close()
    return {"message": "Contact added!", "name": name, "phone": phone}


@app.get("/contacts/delete/{id}")
def delete_contact(id: int):
    conn = get_db()
    conn.execute("DELETE FROM contacts WHERE id = ?", (id,))
    conn.commit()
    conn.close()


@app.get("/contacts/id/{id}")
def get_contact(id: int):
    conn = get_db()
    contact = conn.execute(
        "SELECT * FROM contacts WHERE id = ?", (id,)).fetchone()
    conn.close()
    if contact:
        return {"contact": dict(contact)}
    else:
        return {"message": "Contact not found"}


@app.get("/contacts/update/{id}/{phone}")
def update_contact(id: int, phone: str):
    conn = get_db()
    conn.execute("UPDATE contacts set phone = ? WHERE id =?", (phone, id))
    conn.commit()
    conn.close()
    return {"message": "Contact updated!", "id": id, "phone": phone}
