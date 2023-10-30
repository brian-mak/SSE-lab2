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
                           age=input_age, another_age=output_age,
                           student_id=input_studentid)


def process_query(query):
    if ("dinosaurs" in query):
        return "Dinosaurs ruled the Earth 200 million years ago"

    if ("asteroids" in query):
        return "Unknown"

    if ("What is your name?" in query):
        return "Whatever"

    if ("What is " in query and "plus" in query):
        number_1_start = query.index("is ") + len("is ")
        number_1_end = query.index("plus")
        number_1 = int(query[number_1_start:number_1_end])

        number_2_start = query.index("plus ") + len("plus ")
        number_2_end = query.index("?")
        number_2 = int(query[number_2_start:number_2_end])

        return (number_1 + number_2)


@app.route("/query", methods=["GET"])
def query():
    query_param = request.args.get('q', default='', type=str)
    return process_query(query_param)
