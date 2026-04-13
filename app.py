from flask import Flask, request
import sqlite3
import os

app = Flask(__name__)

# Vulnérabilité 1 : Injection SQL
@app.route("/user")
def get_user():
    username = request.args.get("username", "")
    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE users (id INTEGER, name TEXT, password TEXT)")
    cursor.execute("INSERT INTO users VALUES (1, 'admin', 'secret123')")
    # Requête SQL non paramétrée — volontairement vulnérable
    query = f"SELECT * FROM users WHERE name = '{username}'"
    cursor.execute(query)
    result = cursor.fetchall()
    return str(result)

# Vulnérabilité 2 : Exécution de commande shell
@app.route("/ping")
def ping():
    host = request.args.get("host", "localhost")
    # Injection de commande — volontairement vulnérable
    output = os.popen(f"ping -c 1 {host}").read()
    return f"<pre>{output}</pre>"

@app.route("/")
def index():
    return "Hello, TP Sécurité !"

if __name__ == "__main__":
    app.run(debug=True)
