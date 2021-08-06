from flask import Flask, request
import os

"""
Simple greeting app that runs on Python and flask. It remembers the names and
how often they were encountered, for as long until the app is restarted.
"""

# we can set the port that this app is running on as an environment variable
FL_PORT = os.getenv("FL_PORT") if os.getenv("FL_PORT") else 5000

# This is the "memory" where already encountered names are stored with their
# occurrences
COUNTER = {}

app = Flask(__name__)


@app.route("/")
def index():
    """
    The function generating the main page of the greeting app. Shows a small
    instruction and the already encountered names from the memory.

    Returns
    -------
    str
        HTML string of the main page
    """
    instruct = """
<h2>STUPID GREETING SERVICE</h2>
<ul>
    <li>It will just say hello to you, if you send your name like <code>localhost:{port}/hello/yournamehere</code></li>
</ul>
""".format(port=FL_PORT)
    return instruct + read()


def read():
    """
    Function that generates the view of the already encountered names and
    their occurrences.

    Returns
    -------
    str
        HTML string corresponding to the functionality above.
    """
    s = "<h2>Met people:</h2><ul>"
    for k, v in COUNTER.items():
        s += "<li>{} {} times.</li>".format(k, v)
    s += "</ul>"
    return s


@app.route("/hello/<author>", methods=["GET"])
def send(author):
    """
    If a name is given, it is recorded into COUNTER and subsequently, further
    occurrences of the same name are counted. Also notes other names and
    occurrences.

    Parameters
    ----------
    author: str
        arbitrary name to be greeted, entered as part of the URL in the
        browser.

    Returns
    -------
    str
        HTML string of greeting of the current name as well as other
        encountered names.
    """
    if request.method == "GET":
        au = str(author).lower()
        if au in COUNTER.keys():
            COUNTER[au] += 1
        else:
            COUNTER[au] = 1

        s = "<h3>Hello {}, I have seen you {} times already in my lifetime.</h3>".format(author, COUNTER[au])
        return s + read()


if __name__ == "__main__":
    app.run(port=int(FL_PORT), host="0.0.0.0")
