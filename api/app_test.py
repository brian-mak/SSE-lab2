from app import process_query


def test_knows_about_dinosaurs():
    assert process_query("dinosaurs") == "Dinosaurs ruled the Earth 200 " + \
                                        "million years ago"


def test_does_not_know_about_asteroids():
    assert process_query("asteroids") == "Unknown"


def test_does_not_return_name():
    assert process_query("What is your name?") == "Whatever"


def test_plus():
    assert process_query("What is 32 plus 71?") == "103"

def test_plus():
    assert process_query("Which of the following numbers is the largest: " + \
                         "92, 71, 75?") == '92'

def test_multiply():
    assert process_query("What is 44 multiplied by 48?") == "2112"
