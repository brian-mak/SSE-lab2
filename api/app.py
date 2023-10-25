from flask import Flask, render_template, request
app = Flask(__name__)


@app.route("/")
def hello_world():
    return render_template("index.html")


@app.route("/submit", methods=["POST"])
def submit():
    input_name = request.form.get("name")
    input_age = request.form.get("age")
    input_studentid = request.form.get("studentid")
    output_age = int(input_age) + 25
    return render_template("hello.html", name=input_name,
                           age=input_age, another_age=output_age, student_id=input_studentid)


def process_query(query):
    if (query == "dinosaurs"):
        return "Dinosaurs ruled the Earth 200 million years ago"

    if (query == "asteroids"):
        return "Unknown"


@app.route("/query", methods=["GET"])
def query():
    query_param = request.args.get('q', default='', type=str)
    return process_query(query_param)
