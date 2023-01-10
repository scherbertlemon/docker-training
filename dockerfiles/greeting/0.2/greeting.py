from flask import Flask, request
from datetime import datetime
from database import get_pgconn, insert
import os

"""
Simple greeting app that runs on Python and flask. It remembers the names and
left messages, and stores them into a postgres database.
"""

# Determine the port that this app is running ob via environment
FL_PORT = os.getenv("FL_PORT") if os.getenv("FL_PORT") else 5000

app = Flask(__name__)


@app.route("/")
def index():
    """
    The function generating the main page of the greeting app. Shows a small
    instruction and the already encountered names from the the databse.

    Returns
    -------
    str
        HTML string of the main page
    """
    s = """
<h2>STUPID GREETING SERVICE</h2>
<ul>
    <li>Send GET request like <code>localhost:{port}/hello/yournamehere?message=hello</code></li>
    <li>The service will check how often the entered name has already sent something and list all the messages.</li>
    <li>You can see the already send messages below</li>
</ul>
""".format(port=FL_PORT)
    return s + read()


def read():
    """
    Function that generates the view of the already encountered names and
    messages.

    Returns
    -------
    str
        HTML string corresponding to the functionality above.
    """
    db = get_pgconn()
    try:
        cursor = db.cursor()
        s = "<h2>Received messages</h2><ul>"
        cursor.execute("""
            SELECT LOWER(author), COUNT(*) AS cnt
            FROM messages
            GROUP BY LOWER(author)
            ORDER BY cnt DESC
            """)
        acurs = db.cursor()
        for a, n in cursor.fetchall():
            acurs.execute("""
                SELECT message, received
                FROM messages
                WHERE LOWER(author) = %(author)s
                ORDER BY received DESC
                """,
                {"author": a}
            )
            messages = acurs.fetchall()
            s += "<li>Have seen <b>{}</b> already {} times. Messages:".format(a, n)
            s += "<ul>{}</ul>".format("".join(["<li>'{}' on {}</li>".format(mes, rec) for mes, rec in messages]))
        s += "</ul>"
    finally:
        db.close()
    return s


@app.route("/hello/<author>", methods=["GET"])
def send(author):
    """
    If a name and optionally a message is given, it is recorded into the
    database. A transcript of the recorded information is printed afterwards.

    Parameters
    ----------
    author: str
        arbitrary name to be greeted, entered as part of the URL in the
        browser.

    Returns
    -------
    str
        HTML string of transcript of recorded information.
    """
    if request.method == "GET":
        allowed_keys = ["author", "message", "received"]
        ins = {k: request.args.get(k, default="") for k in allowed_keys}
        now = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        ins["author"] = author
        ins["received"] = now

        s = "<h2>Sending to DB:</h2><ul>"
        for k, v in ins.items():
            s += "<li>{}: {}</li>".format(k, v)
        s += "</ul>"

        db = get_pgconn()
        try:
            insert(db, ins)
        finally:
            db.close()
        return s


if __name__ == "__main__":
    app.run(port=int(FL_PORT), host="0.0.0.0")
