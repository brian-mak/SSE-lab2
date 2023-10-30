from flask import Flask, render_template, request
import re
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
        return str(plus_two_numbers(query))

    if ("Which of the following numbers is the largest:") in query:
        return find_largest_number(query)

    if ("What is " in query and "multiplied by " in query):
        return str(multiply_two_numbers(query))

    if ("Which of the following numbers is both a square and a cube") in query:
        return find_square_and_cube_numbers(query)

    if ("Which of the following numbers are primes: ") in query:
        return find_prime(query)


def is_square_and_cube(number):
    root = int(number ** (1/6))  # Take the 6th root to check for square and cube
    return (root ** 2) ** 3 == number  # Check if the number is both a square and a cube


def find_square_and_cube_numbers(query):
    # Use regular expression to extract numbers from the query
    numbers = [int(match) for match in re.findall(r'\d+', query)]
    if not numbers:
        return []  # No numbers found in the query
    square_and_cube_numbers = [num for num in numbers if is_square_and_cube(num)]
    return str(square_and_cube_numbers)


def plus_two_numbers(query):
    number_1_start = query.index("is ") + len("is ")
    number_1_end = query.index("plus")
    number_1 = int(query[number_1_start:number_1_end])

    number_2_start = query.index("plus ") + len("plus ")
    number_2_end = query.index("?")
    number_2 = int(query[number_2_start:number_2_end])

    return (number_1 + number_2)


def multiply_two_numbers(query):
    number_1_start = query.index("is ") + len("is ")
    number_1_end = query.index("multiplied")
    number_1 = int(query[number_1_start:number_1_end])

    number_2_start = query.index("multiplied by ") + len("multiplied by ")
    number_2_end = query.index("?")
    number_2 = int(query[number_2_start:number_2_end])

    return (number_1 * number_2)


def find_largest_number(query):
    numbers = [int(match) for match in re.findall(r'\d+', query)]
    if not numbers:
        return None  # No numbers found in the query
    # Find the largest number using the max() function
    largest_number = max(numbers)
    return str(largest_number)


def find_prime(query):
    # Use regular expression to extract numbers from the query
    numbers = [int(match) for match in re.findall(r'\d+', query)]
    if not numbers:
        return []  # No numbers found in the query
    prime = [num for num in numbers if is_prime(num)]
    return str(prime[0])


def is_prime(num):
    if num == 1:
        return False
    elif num > 1:
        # check for factors
        for i in range(2, num):
            if (num % i) == 0:
                # if factor is found, set flag to True
                return False
                # break out of loop
                break

        return True


@app.route("/query", methods=["GET"])
def query():
    query_param = request.args.get('q', default='', type=str)
    return process_query(query_param)
