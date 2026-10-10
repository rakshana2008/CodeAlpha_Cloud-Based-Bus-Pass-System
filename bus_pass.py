from flask import Flask, request, jsonify
import sqlite3
import uuid

app = Flask(__name__)

ROUTES = {"Route A": 20, "Route B": 35, "Route C": 50}

def setup():
    with sqlite3.connect("bus.db") as db:
        db.execute("""CREATE TABLE IF NOT EXISTS tickets(
            id TEXT PRIMARY KEY, name TEXT, route TEXT,
            price INTEGER)""")

@app.route("/")
def home():
    return jsonify({"project": "Cloud Bus Pass System",
                    "routes": ROUTES})

@app.route("/book", methods=["POST"])
def book():
    data = request.get_json()
    name = data.get("name", "").strip()
    route = data.get("route", "")

    if not name or route not in ROUTES:
        return jsonify({"error": "Invalid details"}), 400

    ticket = str(uuid.uuid4())
    price = ROUTES[route]

    with sqlite3.connect("bus.db") as db:
        db.execute("INSERT INTO tickets VALUES(?,?,?,?)",
                   (ticket, name, route, price))

    return jsonify({"ticket": ticket, "price": price})

@app.route("/ticket/<ticket>")
def verify(ticket):
    with sqlite3.connect("bus.db") as db:
        result = db.execute(
            "SELECT * FROM tickets WHERE id=?", (ticket,)
        ).fetchone()

    return (jsonify(result) if result
            else (jsonify({"error": "Ticket not found"}), 404))

if __name__ == "__main__":
    setup()
    app.run(debug=False)
