from flask import Flask, render_template, request
import re
import requests
app = Flask(__name__)


@app.route("/")
def welcome():
    return render_template("index.html")


@app.route("/submit_git_repo", methods=["POST"])
def submit_git_repo():
    input_username = request.form.get("git_username")
    response = requests.get("https://api.github.com/users/" +
                            input_username + "/repos")
    if response.status_code == 200:
        repos = response.json()
        repo_info = []
        for repo in repos:
            repo_name = repo["full_name"]
            last_updated = repo["updated_at"]
            commit_response = requests.get("https://api.github.com/repos/" +
                                           repo_name + "/commits")
            if commit_response.status_code == 200:
                commits = commit_response.json()
                if len(commits) > 0:
                    total_commits = len(commits)
                    latest_commit_hash = commits[0]["sha"]
                    latest_commit_date = commits[0]["commit"]["author"]["date"]
                    latest_commit_author = \
                        commits[0]["commit"]["author"]["name"]
                    latest_commit_msg = commits[0]["commit"]["message"]
                else:
                    total_commits = "No commits"
                    latest_commit_hash = "N/A"
                    latest_commit_date = "N/A"
                    latest_commit_author = "N/A"
                    latest_commit_msg = "N/A"
            else:
                latest_commit_hash = "Error fetching commits"
                latest_commit_date = "N/A"
                latest_commit_author = "N/A"
                latest_commit_msg = "N/A"
            repo_info.append((repo_name, last_updated, total_commits,
                              latest_commit_hash, latest_commit_date,
                              latest_commit_author, latest_commit_msg))
        return render_template("repos.html", username=input_username,
                               repo_info=repo_info)
    else:
        error_message = "Error retrieving information. Please check input."
        return error_message


@app.route("/submit_search_keyword", methods=["POST"])
def submit_search_keyword():
    input_username = request.form.get("git_username")
    input_repo_name = request.form.get("repo_name")
    input_keyword = request.form.get("keyword")
    repo_full_name = input_username + "/" + input_repo_name
    commit_response_2 = requests.get("https://api.github.com/repos/" +
                                     repo_full_name + "/commits")
    if commit_response_2.status_code == 200:
        commits_of_interest = commit_response_2.json()
        commits_with_keyword = []
        for commit in commits_of_interest:
            commit_hash = commit["sha"]
            commit_date = commit["commit"]["author"]["date"]
            commit_author = commit["commit"]["author"]["name"]
            commit_msg = commit["commit"]["message"]
            if input_keyword in commit_msg:
                commits_with_keyword.append((commit_hash, commit_date,
                                             commit_author, commit_msg))
        return render_template("search_keyword.html", username=input_username,
                               commits_with_keyword=commits_with_keyword)
    else:
        commits_with_keyword = []
        error_message = "Error retrieving information. Please check input."
        return error_message


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
    root = int(number ** (1/6))
    # Take the 6th root to check for square and cube
    return (root ** 2) ** 3 == number
    # Check if the number is both a square and a cube


def find_square_and_cube_numbers(query):
    # Use regular expression to extract numbers from the query
    numbers = [int(match) for match in re.findall(r'\d+', query)]
    if not numbers:
        return []  # No numbers found in the query
    square_and_cube_numbers = [num for num in numbers if
                               is_square_and_cube(num)]
    result = ",".join(map(str, square_and_cube_numbers))
    return result


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
