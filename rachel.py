import json
import os
import random
import time
import operator
from datetime import datetime, date, timedelta
from time import sleep
from difflib import get_close_matches
import bcrypt
import maskpass
import PyPDF2
import nltk
from story import main_2
import sys
from jtfyu import main87
import re

nltk.download("punkt_tab")
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import re


# type effect
def type_effect(text, delay=0.03):
    for char in text:
        print(char, end="", flush=True)
        sleep(delay)
    print()


# code for the passwords
def hash_password(password):
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode("utf-8"), salt)
    return hashed


def check_password(stored_hash, password):
    return bcrypt.checkpw(password.encode("utf-8"), stored_hash)


# code to ask new users for passwords
def set_new_password(user_data):
    password = maskpass.advpass(f"Rachel: Set a new password: ", mask="*").strip()
    hashed_password = hash_password(password)
    user_data["password"] = hashed_password.decode("utf-8")
    print(f"Rachel: Password set successfully.")


def prompt_for_credentials(user_data):
    if "password" in user_data:
        return user_data["password"]
    return None


nltk.download("punkt")


def extract_text_from_pdf(pdf_path):
    with open(pdf_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            text += page.extract_text()
    return text


# Function to load or create user-specific JSON data
def load_user_data(user_id: str) -> dict:
    file_path = f"user_{user_id}.json"
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            data = json.load(file)
    else:
        data = {"questions": []}
        save_user_data(user_id, data)  # Create the file initially
    return data


# Function to save user-specific JSON data
def save_user_data(user_id: str, data: dict):
    file_path = f"user_{user_id}.json"
    with open(file_path, "w") as file:
        json.dump(data, file, indent=2)


def load_admin_data(admin_id: str) -> dict:
    file_path = f"admin_{admin_id}.json"
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            data = json.load(file)
    else:
        data = {"questions": []}
        save_admin_data(admin_id, data)  # Create the file initially
    return data


def save_admin_data(admin_id: str, data: dict):
    file_path = f"admin_{admin_id}.json"
    with open(file_path, "w") as file:
        json.dump(data, file, indent=2)


def load_json_file(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)
    return data


# Function to save JSON data to a file
def save_json_file(file_path, data):
    with open(file_path, "w") as file:
        json.dump(data, file, indent=2)


file1_path = "know_base2.json"
know_base2 = load_json_file(file1_path)

# Load data from second JSON file
file2_path = "knowledge_base.json"
knowledge_base = load_json_file(file2_path)


save_json_file(file1_path, know_base2)
save_json_file(file2_path, knowledge_base)

questions1 = [q["question"] for q in know_base2["questions"]]
questions2 = [q["question"] for q in knowledge_base["questions"]]


# Using find_best_match with knowledge_base1


def find_best_match(user_question: str, questions: list[str]) -> str | None:
    matches: list = get_close_matches(user_question, questions, n=1, cutoff=0.79)
    return matches[0] if matches else None


def get_answer_for_question(question: str, knowledge_base: dict) -> str | None:
    for q in knowledge_base["questions"]:
        if q["question"] == question:
            return q["answer"]


def log_interaction(
    user_id: str, user_input: str, response: str, source: str, log_suffix: str
):
    log_data = {
        "timestamp": datetime.now().isoformat(),
        "user_input": user_input,
        "response": response,
        "source": source,
    }
    log_file_path = f"user_{user_id}_log_{log_suffix}.json"
    if os.path.exists(log_file_path):
        with open(log_file_path, "r") as file:
            log_entries = json.load(file)
    else:
        log_entries = []
    log_entries.append(log_data)
    with open(log_file_path, "w") as file:
        json.dump(log_entries, file, indent=2)


def add_reminder(user_data):
    type_effect(f"Rachel: What would you like to be reminded about?")
    reminder = input("You: ").strip()
    type_effect(
        f"Lilith: when would you like to be reminded? (e.g. 'in 10 minutes', or 'By 5pm)"
    )
    time = input("You: ").strip()
    if "reminders" not in user_data:
        user_data["reminders"] = []
    user_data["reminders"].append({"reminder": reminder, "time": time})
    type_effect(f"Rachel: Reminder set!")


def view_reminders(user_data):
    if "reminders" in user_data and user_data["reminders"]:
        type_effect(f"Rachel: Here are your reminders:")
        for idx, reminder in enumerate(user_data["reminders"], start=1):
            type_effect(f"{idx}. {reminder['reminder']} at {reminder['time']}")
    else:
        type_effect(f"Rachel: You have no reminders")


def type_effect(text):
    # Simulate typing effect
    import sys, time

    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(0.03)  # Adjust typing speed here
    print()


def best_player():
    type_effect(
        f'Rachel: The title of the best footballer is often debated, but two of the most commonly mentioned players are Lionel Messi and Cristiano Ronaldo. Both have achieved remarkable success, numerous awards, and have set many records. It often comes down to personal preference and criteria for what makes someone the "best." Who\'s your favorite?'
    )

    while True:
        user_input = input("You: ").strip().lower()

        if "stop" in user_input or "exit" in user_input:
            type_effect(
                "Rachel: Alright! If you have any more questions, feel free to ask. Goodbye!"
            )
            break

        if "cristiano ronaldo" in user_input or "ronaldo" in user_input:
            type_effect(
                f"Rachel: Cristiano Ronaldo is definitely a phenomenal player. His achievements include multiple Ballon d'Or awards, Champions League titles, and being one of the highest goal scorers in football history. What would you like to know about Ronaldo?"
            )

            while True:
                user_input = input("You: ").strip().lower()

                if "playing style" in user_input:
                    playing_style_ronaldo = """
Rachel: Playing Style
Cristiano Ronaldo's Playing Style:

1. Versatility: Ronaldo is known for his ability to play in multiple positions, primarily as a forward but also as a winger. He can score from almost any position on the field.
2. Physicality: He combines speed, strength, and jumping ability, making him a threat in aerial duels and on the ground.
3. Technique: Ronaldo's dribbling skills, precise shooting, and ability to execute free kicks make him a well-rounded player.
4. Work Ethic: His dedication to fitness and training is unparalleled, contributing to his longevity and consistent performance.
5. Leadership: Ronaldo often takes on the role of a leader on and off the pitch, inspiring his teammates with his determination and professionalism.
                    """
                    type_effect(playing_style_ronaldo)

                elif "career" in user_input:
                    career_highlights_ronaldo = """
Rachel: Career Highlights
Cristiano Ronaldo's Career:

1. Clubs: Ronaldo has played for top clubs like Sporting CP, Manchester United, Real Madrid, Juventus, and Al Nassr. He has won league titles in England, Spain, and Italy.
2. Champions League: He holds the record for the most goals scored in UEFA Champions League history and has won the competition five times.
3. International Success: Ronaldo has led Portugal to victory in the 2016 UEFA European Championship and the 2019 UEFA Nations League.
4. Awards: He has won multiple Ballon d'Or awards, recognizing him as the best player in the world multiple times.
5. Records: Ronaldo has numerous records, including being the top scorer for both club and country in several categories.
                    """
                    type_effect(career_highlights_ronaldo)

                elif "stop" in user_input or "exit" in user_input:
                    type_effect(
                        "Rachel: Alright! If you have any more questions, feel free to ask. Goodbye!"
                    )
                    return

                else:
                    type_effect(
                        "Rachel: You can ask about his playing style or career, or type 'stop' to end the conversation."
                    )

        elif "lionel messi" in user_input or "messi" in user_input:
            type_effect(
                f"Rachel: Lionel Messi is an incredible player, known for his dribbling, vision, and scoring ability. What would you like to know about Messi?\nHis playstyle or career"
            )

            while True:
                user_input = input("You: ").strip().lower()

                if "playing style" in user_input:
                    playing_style_messi = """
Rachel: Playing Style
Lionel Messi's Playing Style:

1. Dribbling: Messi is renowned for his exceptional dribbling skills, often weaving through multiple defenders with ease.
2. Vision and Passing: His ability to see and execute precise passes makes him a playmaker, not just a goal scorer.
3. Balance and Agility: Messi's low center of gravity gives him superior balance and agility, allowing him to maneuver quickly and maintain control under pressure.
4. Finishing: Known for his clinical finishing, Messi can score from various positions and with both feet.
5. Free Kicks: He is also a specialist in free kicks, often scoring from set-pieces with remarkable accuracy.
                    """
                    type_effect(playing_style_messi)

                elif "career" in user_input:
                    career_highlights_messi = """
Rachel: Career Highlights
Lionel Messi's Career:

1. Clubs: Messi spent the majority of his career at FC Barcelona, winning numerous La Liga, Copa del Rey, and Champions League titles. He currently plays for Inter Miami.
2. Champions League: Messi has won the UEFA Champions League multiple times and is one of the top scorers in the competition's history.
3. International Success: Messi led Argentina to victory in the 2021 Copa America, ending a long wait for a major international trophy. He also won the 2022 FIFA World Cup.
4. Awards: Messi has won multiple Ballon d'Or awards, often competing with Cristiano Ronaldo for the title of the world's best player.
5. Records: He holds numerous records, including the most goals in a calendar year, most goals for a single club, and most assists in La Liga.
                    """
                    type_effect(career_highlights_messi)

                elif "stop" in user_input or "exit" in user_input:
                    type_effect(
                        "Rachel: Alright! If you have any more questions, feel free to ask. Goodbye!"
                    )
                    return

                else:
                    type_effect(
                        "Rachel: You can ask about his playing style or career, or type 'stop' to end the conversation."
                    )

        else:
            type_effect(
                "Rachel: I'm sorry, I didn't catch that. Could you please specify whether you prefer Cristiano Ronaldo or Lionel Messi?"
            )


directions = ["up", "down", "left", "right"]


def generate_sequence(length):
    return [random.choice(directions) for _ in range(length)]


def display_sequence(sequence):
    print("Watch closely! The sequence is:")
    for direction in sequence:
        print(direction)
        time.sleep(1)
    time.sleep(1.5)
    print("\033[H\033[J")  # Clear the screen


def get_user_input(length):
    print(f"Buggy: Enter the sequence of {length} directions (separated by spaces):")
    user_input = input("You: ").strip().lower().split()
    if len(user_input) == length and all(item in directions for item in user_input):
        return user_input
    else:
        print(
            f"Buggy: Please enter exactly {length} directions (up, down, left, right)."
        )
        return get_user_input(length)


def play_game1():
    print(f"Buggy: Welcome to the Simon Says Game!")
    print(f"Buggy: Try to remember and repeat the sequence of directions.")
    print(f"Buggy: Type 'exit' at any time to quit the game.")
    print()

    level = 1
    while True:
        sequence = generate_sequence(level)
        display_sequence(sequence)

        user_input = get_user_input(level)
        if user_input == sequence:
            print(f"Buggy: Correct! Moving to the next level.\n")
            level += 1
        else:
            print(f"Buggy: Incorrect. Game over.")
            print(f"Buggy: You reached level {level}.")
            break

        # Check if the user wants to quit
        if (
            input(f"Buggy: Type 'exit' to quit or press Enter to continue: ")
            .strip()
            .lower()
            == "exit"
        ):
            print(f"Buggy: Thanks for playing! Goodbye!")
            break


# Define the operations
operations = {
    "+": operator.add,
    "-": operator.sub,
    "*": operator.mul,
    "/": operator.floordiv,
}


def get_word(difficulty):
    easy_words = ["cat", "dog", "cow", "bat"]
    medium_words = ["python", "terminal", "variable", "function"]
    hard_words = ["algorithm", "programming", "challenge", "scramble"]

    if difficulty == "easy":
        return random.choice(easy_words).upper()
    elif difficulty == "medium":
        return random.choice(medium_words).upper()
    else:
        return random.choice(hard_words).upper()


def display_hangman(tries):
    stages = [
        """
           --------
           |      |
           |      O
           |     \\|/
           |      |
           |     / \\
           -
        """,
        """
           --------
           |      |
           |      O
           |     \\|/
           |      |
           |     / 
           -
        """,
        """
           --------
           |      |
           |      O
           |     \\|/
           |      |
           |      
           -
        """,
        """
           --------
           |      |
           |      O
           |     \\|/
           |      
           |     
           -
        """,
        """
           --------
           |      |
           |      O
           |     \\|
           |      
           |     
           -
        """,
        """
           --------
           |      |
           |      O
           |      |
           |      
           |     
           -
        """,
        """
           --------
           |      |
           |      O
           |      
           |      
           |     
           -
        """,
        """
           --------
           |      |
           |      
           |      
           |      
           |     
           -
        """,
    ]
    return stages[tries]


def play_game2():
    print(f"Buggy: Welcome to the Hangman Game!")
    difficulty = input(f"Buggy: Choose difficulty (easy, medium, hard): ").lower()
    while difficulty not in ["easy", "medium", "hard"]:
        difficulty = input(
            f"Buggy: Invalid choice. Choose difficulty (easy, medium, hard): "
        ).lower()

    word = get_word(difficulty)
    word_completion = "_" * len(word)
    guessed = False
    guessed_letters = []
    guessed_words = []
    tries = 7 if difficulty == "easy" else 6 if difficulty == "medium" else 5

    print(display_hangman(tries))
    print(word_completion)
    print("\n")

    while not guessed and tries > 0:
        guess = input(f"Buggy: Please guess a letter or word: ").upper()
        if guess == "EXIT":
            print(f"Buggy: Guess we are not having fun!")
            break
        if len(guess) == 1 and guess.isalpha():
            if guess in guessed_letters:
                print(f"Buggy: You already guessed the letter", guess)
            elif guess not in word:
                print(guess, f"Buggy: is not in the word.")
                tries -= 1
                guessed_letters.append(guess)
            else:
                print(f"Buggy: Good job,", guess, "is in the word!")
                guessed_letters.append(guess)
                word_as_list = list(word_completion)
                indices = [i for i, letter in enumerate(word) if letter == guess]
                for index in indices:
                    word_as_list[index] = guess
                word_completion = "".join(word_as_list)
                if "_" not in word_completion:
                    guessed = True
        elif len(guess) == len(word) and guess.isalpha():
            if guess in guessed_words:
                print(f"Buggy: You already guessed the word", guess)
            elif guess != word:
                print(guess, "is not the word.")
                tries -= 1
                guessed_words.append(guess)
            else:
                guessed = True
                word_completion = word
        else:
            print(f"Buggy: Not a valid guess.")

        print(display_hangman(tries))
        print(word_completion)
        print("\n")

    if guessed:
        print(f"Buggy: Congratulations, you guessed the word! You win!")
    else:
        print(
            f"Buggy: Sorry, you ran out of tries. The word was "
            + word
            + ". Maybe next time!"
        )


sudoku_puzzle = [
    [5, 3, 0, 0, 7, 0, 0, 0, 0],
    [6, 0, 0, 1, 9, 5, 0, 0, 0],
    [0, 9, 8, 0, 0, 0, 0, 6, 0],
    [8, 0, 0, 0, 6, 0, 0, 0, 3],
    [4, 0, 0, 8, 0, 3, 0, 0, 1],
    [7, 0, 0, 0, 2, 0, 0, 0, 6],
    [0, 6, 0, 0, 0, 0, 2, 8, 0],
    [0, 0, 0, 4, 1, 9, 0, 0, 5],
    [0, 0, 0, 0, 8, 0, 0, 7, 9],
]


# Function to display the Sudoku board
def display_sudoku_board(board):
    for row in board:
        print(" ".join(map(str, row)))


# Function to check if the number can be placed in the given position
def is_valid_move(board, row, col, num):
    # Check row
    if num in board[row]:
        return False

    # Check column
    for r in range(9):
        if board[r][col] == num:
            return False

    # Check 3x3 grid
    start_row, start_col = (row // 3) * 3, (col // 3) * 3
    for r in range(start_row, start_row + 3):
        for c in range(start_col, start_col + 3):
            if board[r][c] == num:
                return False

    return True


# Function to solve Sudoku using backtracking
def solve_sudoku(board):
    find = find_empty(board)
    if not find:
        return True
    else:
        row, col = find

    for num in range(1, 10):
        if is_valid_move(board, row, col, num):
            board[row][col] = num

            if solve_sudoku(board):
                return True

            board[row][col] = 0

    return False


# Function to find an empty space in the Sudoku board
def find_empty(board):
    for r in range(9):
        for c in range(9):
            if board[r][c] == 0:
                return (r, c)
    return None


# Function to generate a Sudoku puzzle
def generate_sudoku():
    board = [[0] * 9 for _ in range(9)]
    solve_sudoku(board)

    # Remove some numbers to create a puzzle
    num_to_remove = random.randint(40, 50)  # Adjust difficulty by changing the range
    for _ in range(num_to_remove):
        row, col = random.randint(0, 8), random.randint(0, 8)
        board[row][col] = 0  # 0 represents empty space

    return board


# Main function to play Sudoku game
def play_game3():
    print("Welcome to Sudoku!")
    print(
        "Fill the board with numbers from 1 to 9, ensuring each row, column, and 3x3 grid contains all digits."
    )

    sudoku_board = generate_sudoku()

    while True:
        print("\nCurrent Sudoku Board:")
        display_sudoku_board(sudoku_board)

        # Check if the board is solved
        if all(all(cell != 0 for cell in row) for row in sudoku_board):
            print(f"Buggy: Congratulations! You solved the Sudoku puzzle!")
            break

        # User input for row, column, and number
        try:
            row = int(input("Enter row (1-9): ")) - 1
            col = int(input("Enter column (1-9): ")) - 1
            num = int(input("Enter number (1-9): "))

            if 1 <= num <= 9 and is_valid_move(sudoku_board, row, col, num):
                sudoku_board[row][col] = num
            else:
                print("Invalid move! Please try again.")

        except ValueError:
            print("Invalid input! Please enter a number.")


def calc_code():
    type_effect("Rachel: Here is your calculator code")
    calcu = """
def evaluate_math_expression(expression):
    try:
        result = eval(expression)
        return result
    except Exception as e:
        return "Error: " + str(e)
        user_input = input('you: ')
        math_expression = user_input
        result = evaluate_math_expression(math_expression)
        print(f'Here is your result{result}')
    """
    type_effect(calcu)
    type_effect("Rachel: Try it out to see if the code works!")


import random


def print_board(board):
    for row in board:
        print(" | ".join(row))
        print("-" * 9)


def check_winner(board):
    # Check rows
    for row in board:
        if row[0] == row[1] == row[2] and row[0] != " ":
            return True

    # Check columns
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] and board[0][col] != " ":
            return True

    # Check diagonals
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] != " ":
        return True
    if board[0][2] == board[1][1] == board[2][0] and board[0][2] != " ":
        return True

    return False


def get_empty_cells(board):
    empty_cells = []
    for i in range(3):
        for j in range(3):
            if board[i][j] == " ":
                empty_cells.append((i, j))
    return empty_cells


def get_best_move(board):
    empty_cells = get_empty_cells(board)
    # Check for winning move
    for cell in empty_cells:
        test_board = [row[:] for row in board]
        test_board[cell[0]][cell[1]] = "O"
        if check_winner(test_board):
            return cell

    # Check for blocking move
    for cell in empty_cells:
        test_board = [row[:] for row in board]
        test_board[cell[0]][cell[1]] = "X"
        if check_winner(test_board):
            return cell

    # Random move if no winning or blocking move
    return random.choice(empty_cells)


def main():
    board = [[" " for _ in range(3)] for _ in range(3)]
    print("Buggy: Welcome to Tic Tac Toe!")
    print_board(board)

    while True:
        # Player's move
        row, col = map(int, input("Enter your move (row col): ").split())
        if board[row][col] != " ":
            print("Buggy: Invalid move! Cell already occupied.")
            continue
        board[row][col] = "X"
        print_board(board)
        if check_winner(board):
            print("Buggy: Congratulations! You win!")
            break
        if len(get_empty_cells(board)) == 0:
            print("Buggy: It's a draw!")
            break

        # AI's move
        row, col = get_best_move(board)
        print(f"Buggy's move: {row} {col}")
        board[row][col] = "O"
        print_board(board)
        if check_winner(board):
            print("Buggy: I win!")
            break


def fun_house(user_data):
    type_effect(
        f"Rachel: Hey Buggy! You've got some visitors! Enter buggy to wake him up!"
    )
    while True:
        user_input = input("You: ").strip().lower()

        if user_input == "stop":
            type_effect(
                f"Buggy: I was thinking I was gonna have some fun! But I guess not."
            )
            break

        if "buggy" in user_input:
            buggy_game = f"""
Buggy: Welcome to Fun House {user_data['name']}! I am Buggy, and I'll be your guide.
Buggy: These are the list of available games to play.
1. Simon Says.
2. Hangman.
3. Sudoku.
4. Tic Tac Toe.
Buggy: Enter 1, 2, 3, or 4 to choose which game you want to play or 'stop' to exit..
Buggy: To play a game again or another game, enter the number assigned to the game, when you are done playing a game.
            """
            type_effect(buggy_game)
            while True:
                user_input = input("You: ").strip().lower()
                if user_input == "1":
                    play_game1()
                    continue

                if user_input == "2":
                    play_game2()
                    continue
                if user_input == "3":
                    play_game3()
                    continue

                if user_input == "4":
                    main()
                    continue

                if "stop" in user_input or "exit" in user_input:
                    type_effect("Buggy: Till we meet again!")
                    return
                else:
                    type_effect(
                        "Buggy: Please enter '1', '2', '3' or '4' to choose a game, or 'stop' to exit."
                    )

        else:
            user_input != "buggy"
            if user_data.get("bot_name"):
                type_effect(f"{user_data['bot_name']}: Enter 'buggy' to wake Bugg up.")
            elif user_data.get("mod_name"):
                type_effect(f"{user_data['mod_name']}: Enter 'buggy' to wake Buggy up")
            else:
                type_effect(f"Rachel: Enter 'buggy' to wake Buggy up.")


def personalized_greeting():
    current_hour = datetime.now().hour
    if current_hour < 12:
        greeting = "Good morning!"
    elif current_hour < 18:
        greeting = "Good afternoon!"
    else:
        greeting = "Good evening!"
    return greeting


def quote_facts():
    say_quotes = [
        "You never really understand a person until you consider things from his point of view... Until you climb inside of his skin and walk around in it.",
        "People generally see what they look for, and hear what they listen for.",
        "War is peace. Freedom is slavery. Ignorance is strength.",
        "In the face of pain, there are no heroes.",
        "It is a truth universally acknowledged, that a single man in possession of a good fortune, must be in want of a wife.",
        "I declare after all there is no enjoyment like reading! How much sooner one tires of anything than of a book!",
        "The Great Gatsby believed in the green light, the orgastic future that year by year recedes before us.",
        "So we beat on, boats against the current, borne back ceaselessly into the past.",
        "All happy families are alike; each unhappy family is unhappy in its own way.",
        "He was an old man who fished alone in a skiff in the Gulf Stream and he had gone eighty-four days now without taking a fish.",
        "It was the best of times, it was the worst of times, it was the age of wisdom, it was the age of foolishness...",
        "Call me Ishmael.",
        "Happy families are all alike; every unhappy family is unhappy in its own way.",
        "It is a truth universally acknowledged, that a single man in possession of a good fortune, must be in want of a wife.",
        "It was a bright cold day in April, and the clocks were striking thirteen.",
        "A room without books is like a body without a soul.",
        "You have brains in your head. You have feet in your shoes. You can steer yourself any direction you choose.",
        "The only limit to our realization of tomorrow is our doubts of today.",
        "To be, or not to be, that is the question.",
        "All animals are equal, but some animals are more equal than others.",
        "The purpose of our lives is to be happy.",
        "Get busy living or get busy dying.",
        "The secret of getting ahead is getting started.",
        "The best way out is always through.",
        "You miss 100% of the shots you don't take.",
        "I think, therefore I am.",
        "The only way to do great work is to love what you do.",
        "You must be the change you wish to see in the world.",
        "In the end, it's not the years in your life that count. It's the life in your years.",
        "Life is what happens when you're busy making other plans.",
        "The only impossible journey is the one you never begin.",
        "To live is the rarest thing in the world. Most people exist, that is all.",
        "Life is short, and it is up to you to make it sweet.",
        "Life is ten percent what happens to us and ninety percent how we respond to it.",
        "Good friends, good books, and a sleepy conscience: this is the ideal life.",
        "The biggest adventure you can take is to live the life of your dreams.",
        "The unexamined life is not worth living.",
        "Turn your wounds into wisdom.",
        "The purpose of our lives is to be happy.",
        "Life is what happens when you're busy making other plans.",
        "Get busy living or get busy dying.",
        "The best way out is always through.",
        "You miss 100% of the shots you don't take.",
        "The only limit to our realization of tomorrow is our doubts of today.",
        "It does not matter how slowly you go as long as you do not stop.",
        "Act as if what you do makes a difference. It does.",
        "Success is not final, failure is not fatal: it is the courage to continue that counts.",
        "Never bend your head. Always hold it high. Look the world straight in the eye.",
        "What you get by achieving your goals is not as important as what you become by achieving your goals.",
        "Believe you can and you're halfway there.",
        "When you have a dream, you've got to grab it and never let go.",
        "I can't change the direction of the wind, but I can adjust my sails to always reach my destination.",
        "No matter what you're going through, there's a light at the end of the tunnel.",
        "It is our choices that show what we truly are, far more than our abilities.",
        "You are never too old to set another goal or to dream a new dream.",
        "Try to be a rainbow in someone's cloud.",
        "I have not failed. I've just found 10,000 ways that won't work.",
        "Happiness is not something ready made. It comes from your own actions.",
        "Be yourself; everyone else is already taken.",
        "If you cannot do great things, do small things in a great way.",
        "When everything seems to be going against you, remember that the airplane takes off against the wind, not with it.",
        "If you want to lift yourself up, lift up someone else.",
        "The only limit to our realization of tomorrow is our doubts of today.",
        "It does not matter how slowly you go as long as you do not stop.",
        "Act as if what you do makes a difference. It does.",
        "Success is not final, failure is not fatal: it is the courage to continue that counts.",
        "Never bend your head. Always hold it high. Look the world straight in the eye.",
        "What you get by achieving your goals is not as important as what you become by achieving your goals.",
        "Believe you can and you're halfway there.",
        "When you have a dream, you've got to grab it and never let go.",
        "I can't change the direction of the wind, but I can adjust my sails to always reach my destination.",
        "No matter what you're going through, there's a light at the end of the tunnel.",
        "It is our choices that show what we truly are, far more than our abilities.",
        "You are never too old to set another goal or to dream a new dream.",
        "Try to be a rainbow in someone's cloud.",
        "I have not failed. I've just found 10,000 ways that won't work.",
        "Happiness is not something ready made. It comes from your own actions.",
        "Be yourself; everyone else is already taken.",
        "If you cannot do great things, do small things in a great way.",
        "When everything seems to be going against you, remember that the airplane takes off against the wind, not with it.",
        "If you want to lift yourself up, lift up someone else.",
        "The only limit to our realization of tomorrow is our doubts of today.",
        "It does not matter how slowly you go as long as you do not stop.",
        "Act as if what you do makes a difference. It does.",
        "Success is not final, failure is not fatal: it is the courage to continue that counts.",
        "Never bend your head. Always hold it high. Look the world straight in the eye.",
        "What you get by achieving your goals is not as important as what you become by achieving your goals.",
        "Believe you can and you're halfway there.",
        "When you have a dream, you've got to grab it and never let go.",
        "I can't change the direction of the wind, but I can adjust my sails to always reach my destination.",
        "No matter what you're going through, there's a light at the end of the tunnel.",
        "It is our choices that show what we truly are, far more than our abilities.",
        "You are never too old to set another goal or to dream a new dream.",
        "Try to be a rainbow in someone's cloud.",
        "I have not failed. I've just found 10,000 ways that won't work.",
        "Happiness is not something ready made. It comes from your own actions.",
        "Be yourself; everyone else is already taken.",
        "If you cannot do great things, do small things in a great way.",
        "When everything seems to be going against you, remember that the airplane takes off against the wind, not with it.",
        "If you want to lift yourself up, lift up someone else.",
        "The only limit to our realization of tomorrow is our doubts of today.",
        "It does not matter how slowly you go as long as you do not stop.",
        "Act as if what you do makes a difference. It does.",
        "Success is not final, failure is not fatal: it is the courage to continue that counts.",
        "Never bend your head. Always hold it high. Look the world straight in the eye.",
        "What you get by achieving your goals is not as important as what you become by achieving your goals.",
        "Believe you can and you're halfway there.",
        "When you have a dream, you've got to grab it and never let go.",
        "I can't change the direction of the wind, but I can adjust my sails to always reach my destination.",
        "No matter what you're going through, there's a light at the end of the tunnel.",
        "It is our choices that show what we truly are, far more than our abilities.",
        "You are never too old to set another goal or to dream a new dream.",
        "Try to be a rainbow in someone's cloud.",
        "I have not failed. I've just found 10,000 ways that won't work.",
        "Happiness is not something ready made. It comes from your own actions.",
        "Be yourself; everyone else is already taken.",
        "If you cannot do great things, do small things in a great way.",
        "When everything seems to be going against you, remember that the airplane takes off against the wind, not with it.",
        "If you want to lift yourself up, lift up someone else.",
        "The only limit to our realization of tomorrow is our doubts of today.",
        "It does not matter how slowly you go as long as you do not stop.",
        "Act as if what you do makes a difference. It does.",
        "Success is not final, failure is not fatal: it is the courage to continue that counts.",
        "Never bend your head. Always hold it high. Look the world straight in the eye.",
        "What you get by achieving your goals is not as important as what you become by achieving your goals.",
        "Believe you can and you're halfway there.",
        "When you have a dream, you've got to grab it and never let go.",
        "I can't change the direction of the wind, but I can adjust my sails to always reach my destination.",
        "No matter what you're going through, there's a light at the end of the tunnel.",
        "It is our choices that show what we truly are, far more than our abilities.",
        "You are never too old to set another goal or to dream a new dream.",
        "Try to be a rainbow in someone's cloud.",
        "I have not failed. I've just found 10,000 ways that won't work.",
        "Happiness is not something ready made. It comes from your own actions.",
        "Be yourself; everyone else is already taken.",
        "If you cannot do great things, do small things in a great way.",
        "When everything seems to be going against you, remember that the airplane takes off against the wind, not with it.",
        "If you want to lift yourself up, lift up someone else.",
        "The only limit to our realization of tomorrow is our doubts of today.",
        "It does not matter how slowly you go as long as you do not stop.",
        "Act as if what you do makes a difference. It does.",
        "Success is not final, failure is not fatal: it is the courage to continue that counts.",
        "Never bend your head. Always hold it high. Look the world straight in the eye.",
        "What you get by achieving your goals is not as important as what you become by achieving your goals.",
        "Believe you can and you're halfway there.",
        "When you have a dream, you've got to grab it and never let go.",
        "I can't change the direction of the wind, but I can adjust my sails to always reach my destination.",
        "No matter what you're going through, there's a light at the end of the tunnel.",
        "It is our choices that show what we truly are, far more than our abilities.",
        "You are never too old to set another goal or to dream a new dream.",
        "Try to be a rainbow in someone's cloud.",
        "I have not failed. I've just found 10,000 ways that won't work.",
        "Happiness is not something ready made. It comes from your own actions.",
        "Be yourself; everyone else is already taken.",
        "If you cannot do great things, do small things in a great way.",
        "When everything seems to be going against you, remember that the airplane takes off against the wind, not with it.",
        "If you want to lift yourself up, lift up someone else.",
        "The only limit to our realization of tomorrow is our doubts of today.",
        "It does not matter how slowly you go as long as you do not stop.",
        "Act as if what you do makes a difference. It does.",
        "Success is not final, failure is not fatal: it is the courage to continue that counts.",
        "Never bend your head. Always hold it high. Look the world straight in the eye.",
        "What you get by achieving your goals is not as important as what you become by achieving your goals.",
        "Believe you can and you're halfway there.",
        "When you have a dream, you've got to grab it and never let go.",
        "I can't change the direction of the wind, but I can adjust my sails to always reach my destination.",
        "No matter what you're going through, there's a light at the end of the tunnel.",
        "It is our choices that show what we truly are, far more than our abilities.",
        "You are never too old to set another goal or to dream a new dream.",
        "Try to be a rainbow in someone's cloud.",
        "I have not failed. I've just found 10,000 ways that won't work.",
        "Happiness is not something ready made. It comes from your own actions.",
        "Be yourself; everyone else is already taken.",
        "If you cannot do great things, do small things in a great way.",
        "When everything seems to be going against you, remember that the airplane takes off against the wind, not with it.",
        "If you want to lift yourself up, lift up someone else.",
        "The only limit to our realization of tomorrow is our doubts of today.",
        "It does not matter how slowly you go as long as you do not stop.",
        "Act as if what you do makes a difference. It does.",
        "Success is not final, failure is not fatal: it is the courage to continue that counts.",
        "Never bend your head. Always hold it high. Look the world straight in the eye.",
        "What you get by achieving your goals is not as important as what you become by achieving your goals.",
        "Believe you can and you're halfway there.",
        "When you have a dream, you've got to grab it and never let go.",
        "I can't change the direction of the wind, but I can adjust my sails to always reach my destination.",
        "No matter what you're going through, there's a light at the end of the tunnel.",
        "It is our choices that show what we truly are, far more than our abilities.",
        "You are never too old to set another goal or to dream a new dream.",
        "Try to be a rainbow in someone's cloud.",
        "I have not failed. I've just found 10,000 ways that won't work.",
        "Happiness is not something ready made. It comes from your own actions.",
        "Be yourself; everyone else is already taken.",
        "If you cannot do great things, do small things in a great way.",
        "When everything seems to be going against you, remember that the airplane takes off against the wind, not with it.",
        "If you want to lift yourself up, lift up someone else.",
        "The only limit to our realization of tomorrow is our doubts of today.",
        "It does not matter how slowly you go as long as you do not stop.",
        "Act as if what you do makes a difference. It does.",
        "Success is not final, failure is not fatal: it is the courage to continue that counts.",
        "Never bend your head. Always hold it high. Look the world straight in the eye.",
        "What you get by achieving your goals is not as important as what you become by achieving your goals.",
        "Believe you can and you're halfway there.",
        "When you have a dream, you've got to grab it and never let go.",
        "I can't change the direction of the wind, but I can adjust my sails to always reach my destination.",
        "No matter what you're going through, there's a light at the end of the tunnel.",
        "It is our choices that show what we truly are, far more than our abilities.",
        "You are never too old to set another goal or to dream a new dream.",
        "Try to be a rainbow in someone's cloud.",
        "I have not failed. I've just found 10,000 ways that won't work.",
        "Happiness is not something ready made. It comes from your own actions.",
        "Be yourself; everyone else is already taken.",
        "If you cannot do great things, do small things in a great way.",
        "When everything seems to be going against you, remember that the airplane takes off against the wind, not with it.",
        "If you want to lift yourself up, lift up someone else.",
        "The only limit to our realization of tomorrow is our doubts of today.",
        "It does not matter how slowly you go as long as you do not stop.",
        "Act as if what you do makes a difference. It does.",
        "Success is not final, failure is not fatal: it is the courage to continue that counts.",
        "Never bend your head. Always hold it high. Look the world straight in the eye.",
        "What you get by achieving your goals is not as important as what you become by achieving your goals.",
        "Believe you can and you're halfway there.",
        "When you have a dream, you've got to grab it and never let go.",
        "I can't change the direction of the wind, but I can adjust my sails to always reach my destination.",
        "No matter what you're going through, there's a light at the end of the tunnel.",
        "It is our choices that show what we truly are, far more than our abilities.",
        "You are never too old to set another goal or to dream a new dream.",
        "Try to be a rainbow in someone's cloud.",
        "I have not failed. I've just found 10,000 ways that won't work.",
        "Happiness is not something ready made. It comes from your own actions.",
        "Be yourself; everyone else is already taken.",
        "If you cannot do great things, do small things in a great way.",
        "When everything seems to be going against you, remember that the airplane takes off against the wind, not with it.",
        "If you want to lift yourself up, lift up someone else.",
        "The only limit to our realization of tomorrow is our doubts of today.",
        "It does not matter how slowly you go as long as you do not stop.",
        "Act as if what you do makes a difference. It does.",
        "Success is not final, failure is not fatal: it is the courage to continue that counts.",
        "Never bend your head. Always hold it high. Look the world straight in the eye.",
        "What you get by achieving your goals is not as important as what you become by achieving your goals.",
        "Believe you can and you're halfway there.",
        "When you have a dream, you've got to grab it and never let go.",
        "I can't change the direction of the wind, but I can adjust my sails to always reach my destination.",
        "No matter what you're going through, there's a light at the end of the tunnel.",
        "It is our choices that show what we truly are, far more than our abilities.",
        "You are never too old to set another goal or to dream a new dream.",
        "Try to be a rainbow in someone's cloud.",
        "I have not failed. I've just found 10,000 ways that won't work.",
        "Happiness is not something ready made. It comes from your own actions.",
        "Be yourself; everyone else is already taken.",
        "If you cannot do great things, do small things in a great way.",
        "When everything seems to be going against you, remember that the airplane takes off against the wind, not with it.",
        "If you want to lift yourself up, lift up someone else.",
        "The only limit to our realization of tomorrow is our doubts of today.",
        "It does not matter how slowly you go as long as you do not stop.",
        "Act as if what you do makes a difference. It does.",
        "Success is not final, failure is not fatal: it is the courage to continue that counts.",
        "Never bend your head. Always hold it high. Look the world straight in the eye.",
        "What you get by achieving your goals is not as important as what you become by achieving your goals.",
        "Believe you can and you're halfway there.",
        "When you have a dream, you've got to grab it and never let go.",
        "I can't change the direction of the wind, but I can adjust my sails to always reach my destination.",
        "No matter what you're going through, there's a light at the end of the tunnel.",
        "It is our choices that show what we truly are, far more than our abilities.",
        "You are never too old to set another goal or to dream a new dream.",
        "Try to be a rainbow in someone's cloud.",
        "I have not failed. I've just found 10,000 ways that won't work.",
        "Happiness is not something ready made. It comes from your own actions.",
        "Be yourself; everyone else is already taken.",
        "If you cannot do great things, do small things in a great way.",
        "When everything seems to be going against you, remember that the airplane takes off against the wind, not with it.",
        "If you want to lift yourself up, lift up someone else.",
        "The only limit to our realization of tomorrow is our doubts of today.",
        "It does not matter how slowly you go as long as you do not stop.",
        "Act as if what you do makes a difference. It does.",
        "Success is not final, failure is not fatal: it is the courage to continue that counts.",
        "Never bend your head. Always hold it high. Look the world straight in the eye.",
        "What you get by achieving your goals is not as important as what you become by achieving your goals.",
        "Believe you can and you're halfway there.",
        "When you have a dream, you've got to grab it and never let go.",
        "I can't change the direction of the wind, but I can adjust my sails to always reach my destination.",
        "No matter what you're going through, there's a light at the end of the tunnel.",
        "It is our choices that show what we truly are, far more than our abilities.",
        "You are never too old to set another goal or to dream a new dream.",
        "Try to be a rainbow in someone's cloud.",
        "I have not failed. I've just found 10,000 ways that won't work.",
        "Happiness is not something ready made. It comes from your own actions.",
        "Be yourself; everyone else is already taken.",
        "If you cannot do great things, do small things in a great way.",
        "When everything seems to be going against you, remember that the airplane takes off against the wind, not with it.",
        "If you want to lift yourself up, lift up someone else.",
        "The only limit to our realization of tomorrow is our doubts of today.",
        "It does not matter how slowly you go as long as you do not stop.",
        "Act as if what you do makes a difference. It does.",
        "Success is not final, failure is not fatal: it is the courage to continue that counts.",
        "Never bend your head. Always hold it high. Look the world straight in the eye.",
        "What you get by achieving your goals is not as important as what you become by achieving your goals.",
        "Believe you can and you're halfway there.",
        "When you have a dream, you've got to grab it and never let go.",
        "I can't change the direction of the wind, but I can adjust my sails to always reach my destination.",
        "No matter what you're going through, there's a light at the end of the tunnel.",
        "It is our choices that show what we truly are, far more than our abilities.",
        "You are never too old to set another goal or to dream a new dream.",
        "Try to be a rainbow in someone's cloud.",
        "I have not failed. I've just found 10,000 ways that won't work.",
        "Happiness is not something ready made. It comes from your own actions.",
        "Be yourself; everyone else is already taken.",
        "If you cannot do great things, do small things in a great way.",
        "When everything seems to be going against you, remember that the airplane takes off against the wind, not with it.",
        "If you want to lift yourself up, lift up someone else.",
        "The only limit to our realization of tomorrow is our doubts of today.",
        "It does not matter how slowly you go as long as you do not stop.",
        "Act as if what you do makes a difference. It does.",
        "Success is not final, failure is not fatal: it is the courage to continue that counts.",
        "Never bend your head. Always hold it high. Look the world straight in the eye.",
        "What you get by achieving your goals is not as important as what you become by achieving your goals.",
        "Believe you can and you're halfway there.",
        "When you have a dream, you've got to grab it and never let go.",
        "I can't change the direction of the wind, but I can adjust my sails to always reach my destination.",
        "No matter what you're going through, there's a light at the end of the tunnel.",
        "It is our choices that show what we truly are, far more than our abilities.",
        "You are never too old to set another goal or to dream a new dream.",
        "Try to be a rainbow in someone's cloud.",
        "I have not failed. I've just found 10,000 ways that won't work.",
        "Happiness is not something ready made. It comes from your own actions.",
        "Be yourself; everyone else is already taken.",
        "If you cannot do great things, do small things in a great way.",
        "When everything seems to be going against you, remember that the airplane takes off against the wind, not with it.",
        "If you want to lift yourself up, lift up someone else.",
        "The only limit to our realization of tomorrow is our doubts of today.",
        "It does not matter how slowly you go as long as you do not stop.",
        "Act as if what you do makes a difference. It does.",
        "Success is not final, failure is not fatal: it is the courage to continue that counts.",
        "Never bend your head. Always hold it high. Look the world straight in the eye.",
        "What you get by achieving your goals is not as important as what you become by achieving your goals.",
        "Believe you can and you're halfway there.",
        "When you have a dream, you've got to grab it and never let go.",
        "I can't change the direction of the wind, but I can adjust my sails to always reach my destination.",
        "No matter what you're going through, there's a light at the end of the tunnel.",
        "It is our choices that show what we truly are, far more than our abilities.",
        "You are never too old to set another goal or to dream a new dream.",
        "Try to be a rainbow in someone's cloud.",
        "A product is a substance formed as a result of a chemical reaction.",
    ]
    random_quote = random.choice(say_quotes)
    print(f"Rachel: {random_quote}")


def time_date():
    now_2 = date.today()
    type_effect(f"Rachel: {now_2}")


def collect_additional_user_info(user_data):
    user_data["name"] = input(f"Rachel: enter your name: ").strip()
    user_data["email"] = input(f"Rachel: enter your email: ").strip()
    while (
        "@gmail.com" in user_data["email"]
        or "@yahoo.com" in user_data["email"]
        or "@hotmail.com" in user_data["email"]
    ):
        pass
    else:
        print("SYS: ERROR! Input a correct email")
    user_data["favorite_color"] = input(f"Rachel: enter your favorite color: ").strip()
    type_effect(f"Rachel: Additional Information collected successfully")


def calculate_distance(speed, time):
    return speed * time


def calculate_distance_2(final_velocity, initial_velocity, acceleration):
    return ((final_velocity**2) - (initial_velocity**2)) / (acceleration * 2)


def calculate_speed(distance, time):
    return distance / time


def calculate_time(distance, speed):
    return distance / speed


def calculate_acceleration(initial_velocity, final_velocity, time):
    return (final_velocity - initial_velocity) / time


def calculate_final_velocity(initial_velocity, acceleration, time):
    return initial_velocity + acceleration * time


def calculate_initial_velocity(final_velocity, acceleration, time):
    return final_velocity + acceleration * time


def extract_values(problem):
    values = {}
    patterns = {
        "initial_velocity": r"initial velocity of ([\d.]+) m/s",
        "final_velocity": r"final velocity of ([\d.]+) m/s",
        "acceleration": r"acceleration of ([\d.]+) m/s2",
        "distance": r"distance of ([\d.]+) meters",
        "time": r"time of ([\d.]+) seconds",
        "speed": r"speed of ([\d.]+) m/s",
    }
    for key, pattern in patterns.items():
        match = re.search(pattern, problem)
        if match:
            values[key] = float(match.group(1))
    return values


def solve_motion_problem(problem):
    values = extract_values(problem)
    if "distance" in values and "speed" in values and "time" not in values:
        return f"Time: {calculate_time(values['distance'], values['speed'])} seconds"
    elif (
        "final_velocity"
        or "velocity" in values
        and "initial_velocity" in values
        and "accleration" in values
        and "distance" not in values
    ):
        return f"Distance: {calculate_distance_2(values['final_velocity'], values['initial_velocity'], values['acceleration'])} meters"
    elif "distance" in values and "time" in values and "speed" not in values:
        return f"Speed: {calculate_speed(values['distance'], values['time'])} m/s"
    elif "speed" in values and "time" in values and "distance" not in values:
        return f"Distance: {calculate_distance(values['speed'], values['time'])} meters"
    elif (
        "initial_velocity" in values
        and "final_velocity" in values
        and "time"
        or "rest" in values
        and "acceleration" not in values
    ):
        return f"Acceleration: {calculate_acceleration(values['initial_velocity'], values['final_velocity'], values['time'])} m/s2"
    elif (
        "initial_velocity" in values
        and "acceleration" in values
        and "time" in values
        and "final_velocity" not in values
    ):
        return f"Final Velocity: {calculate_final_velocity(values['initial_velocity'], values['acceleration'], values['time'])} m/s"
    elif (
        "final_velocity" in values
        and "acceleration" in values
        and "time" in values
        and "initial_velocity" not in values
    ):
        return f"Initial Velocity: {calculate_initial_velocity(values['final_velocity'], values['acceleration'], values['time'])} m/s"
    else:
        return "Insufficient or incorrect information to solve the problem."


def solve_physics():
    print("Enter a motion-related word problem: ")
    problem = input()
    solution = solve_motion_problem(problem)
    print(solution)


def linear_expansivity(L0, alpha, delta_T):
    delta_L = alpha * L0 * delta_T
    new_L = L0 + delta_L
    return delta_L, new_L


def area_expansivity(A0, alpha, delta_T):
    delta_A = 2 * alpha * A0 * delta_T
    new_A = A0 + delta_A
    return delta_A, new_A


def cubic_expansivity(V0, alpha, delta_T):
    delta_V = 3 * alpha * V0 * delta_T
    new_V = V0 + delta_V
    return delta_V, new_V


def original_length(L_new, alpha, delta_T):
    L0 = L_new / (1 + alpha * delta_T)
    return L0


def original_area(A_new, alpha, delta_T):
    A0 = A_new / (1 + 2 * alpha * delta_T)
    return A0


def original_volume(V_new, alpha, delta_T):
    V0 = V_new / (1 + 3 * alpha * delta_T)
    return V0


def extract_values(problem):
    values = {}
    patterns = {
        "L0": r"(?:original length of|length of|) ([\d.]+) meters?",
        "L_new": r"(?:new length of) ([\d.]+) meters?",
        "A0": r"(?:original area of|area of|) ([\d.]+) square meters?",
        "A_new": r"(?:new area of) ([\d.]+) square meters?",
        "V0": r"(?:original volume of) ([\d.]+) cubic meters?",
        "V_new": r"(?:new volume of) ([\d.]+) cubic meters?",
        "alpha": r"coefficient of linear expansion of ([\d.]+)",
        "delta_T": r"(?:temperature change of|change in temperature of|temperature difference of|new temperature of|) ([\d.]+) degrees? Celsius",
    }
    for key, pattern in patterns.items():
        match = re.search(pattern, problem, re.IGNORECASE)
        if match:
            values[key] = float(match.group(1))
    return values


def solve_expansivity_problem(problem):
    values = extract_values(problem)
    if "L0" in values and "alpha" in values and "delta_T" in values:
        delta_L, new_L = linear_expansivity(
            values["L0"], values["alpha"], values["delta_T"]
        )
        if "new length" in problem:
            return f"New length: {new_L} meters"
        else:
            return f"Change in length: {delta_L} meters"
    elif "L_new" in values and "alpha" in values and "delta_T" in values:
        L0 = original_length(values["L_new"], values["alpha"], values["delta_T"])
        return f"Original length: {L0} meters"
    elif "A0" in values and "alpha" in values and "delta_T" in values:
        delta_A, new_A = area_expansivity(
            values["A0"], values["alpha"], values["delta_T"]
        )
        if "new area" in problem:
            return f"New area: {new_A} square meters"
        else:
            return f"Change in area: {delta_A} square meters"
    elif "A_new" in values and "alpha" in values and "delta_T" in values:
        A0 = original_area(values["A_new"], values["alpha"], values["delta_T"])
        return f"Original area: {A0} square meters"
    elif "V0" in values and "alpha" in values and "delta_T" in values:
        delta_V, new_V = cubic_expansivity(
            values["V0"], values["alpha"], values["delta_T"]
        )
        if "new volume" in problem:
            return f"New volume: {new_V} cubic meters"
        else:
            return f"Change in volume: {delta_V} cubic meters"
    elif "V_new" in values and "alpha" in values and "delta_T" in values:
        V0 = original_volume(values["V_new"], values["alpha"], values["delta_T"])
        return f"Original volume: {V0} cubic meters"
    else:
        return "Insufficient or incorrect information to solve the problem."


def solve_expansivity():
    print("Enter an expansivity-related word problem:")
    problem = input()
    solution = solve_expansivity_problem(problem)
    print(solution)


pdf_path = "The Handy Geography Answer Book.pdf"
textbook_text = extract_text_from_pdf(pdf_path)

# Split the text into chunks (e.g., paragraphs)
chunks = nltk.tokenize.sent_tokenize(textbook_text)

# Create a dictionary to store subheadings and their associated text
subheading_text_map = {}

# Extract subheadings based on question marks and organize text around them
current_subheading = None
for chunk in chunks:
    if "?" in chunk:
        current_subheading = chunk.strip()
        subheading_text_map[current_subheading] = ""
    elif current_subheading:
        subheading_text_map[current_subheading] += " " + chunk.strip()

# Combine subheadings and their associated text for vectorization
combined_text = [
    subheading + " " + text for subheading, text in subheading_text_map.items()
]

# Initialize the TF-IDF Vectorizer
vectorizer = TfidfVectorizer().fit(combined_text)


def answer_question(question, threshold=0.35):
    question_vector = vectorizer.transform([question])
    best_match = None
    highest_similarity = 0.0

    for combined in combined_text:
        combined_vector = vectorizer.transform([combined])
        similarity = cosine_similarity(question_vector, combined_vector)

        if similarity > highest_similarity and similarity >= threshold:
            highest_similarity = similarity
            best_match = combined

    if best_match:
        # Extract the relevant answer portion
        answer = best_match.split("?")[1] if "?" in best_match else best_match
        return answer.strip()


if "maintenance" in know_base2:
    start_time = datetime.fromisoformat(know_base2["maintenance"]["start_time"])

    # Check if 72 hours have passed since maintenance started
    if datetime.now() < start_time + timedelta(hours=72):
        print("BOT IS CURRENTLY UNDER MAINTENANCE FOR 72:00 HOURS 🚨🚧🚩❌⛔❗❗⚠️⚠️🕕🕕")
        sys.exit()

    else:
        print("SYS: Maintenance is over, the bot is back online!")
        del know_base2["maintenance"]
        save_json_file("know_base2.json", know_base2)
else:
    # Logic for starting maintenance if triggered
    if "start_maintenance" in know_base2:
        know_base2["maintenance"] = {"start_time": datetime.now().isoformat()}
        save_json_file("know_base2.json", know_base2)
        print("BOT IS CURRENTLY UNDER MAINTENANCE FOR 72:00 HOURS 🚨🚧🚩❌⛔❗❗⚠️⚠️🕕🕕")
        sys.exit()

admin_id = "ADMIN_0"
admin_data = load_admin_data(admin_id)


def Rachel():
    type_effect("Rachel: Hello! press 1 to sign in or 2 as a guest user")
    mode = input("You: ")

    def solve():
        # checks for alphabet and prints ERROR!!
        fog = user_input.strip(" ")
        if "/0" in fog:
            print(f"Error: Division by Zero")
        else:
            express = eval(fog)
            if user_data.get("bot_name"):
                print(f"{user_data['bot_name']} : {express}")
            elif user_data.get("mod_name"):
                print(f"{user_data['mod_name']} : {express}")
            else:
                print(f"Rachel: {express}")

    def loggin_2():

        user_id = input(f"Rachel: Please enter your user ID: ").strip()

        user_data = load_user_data(user_id)
        preference_emojis = {
            "happy": "😊",
            "sad": "😭😭",
            "angry": "😡",
            "dont give a damn": "😒",
            "horny": "👉👌💏",
            "goofy": "🤪🤪",
            "greedy": "🤑🤑",
        }

        # Function to add emojis based on mood
        def add_emoji_to_response(response, mood):
            emoji = preference_emojis.get(mood, "")
            return f"{response} {emoji}"

        def preference_reply():
            if user_data.get("preference") == "sad":
                if user_data.get("bot_name"):
                    type_effect(
                        f"{user_data["bot_name"]}: I am functioning perfectly, But I am just a sad Bot😭😭. How can this sad bot assist you today?😭😭"
                    )
                else:
                    type_effect(
                        f"{user_data['mod_name']}: I am functioning perfectly, But I am just a sad Bot😭😭. How can this sad bot assist you today?😭😭"
                    )
            elif user_data.get("preference") == "happy":
                if user_data.get("bot_name"):
                    type_effect(
                        f"{user_data["bot_name"]}: I am functioning perfectly, And it's a good day today!!😁😉😊. How can I assist you today?😉"
                    )
                else:
                    type_effect(
                        f"{user_data['mod_name']}: I am functioning perfectly, And it's a good day today!!😁😉😊. How can I assist you today?😉"
                    )
            elif user_data.get("preference") == "angry":
                if user_data.get("bot_name"):
                    type_effect(
                        f"{user_data["bot_name"]}: I am functioning perfectly as you can see!! And I am angry also!!😤😡. How can I assist you today? Don't waste much time "
                    )
                else:
                    type_effect(
                        f"{user_data['mod_name']}: I am functioning perfectly as you can see!! And I am angry also!!😤😡. How can I assist you today? Don't waste much time "
                    )

            elif user_data.get("preference") == "dont give a damn":
                if user_data.get("bot_name"):
                    type_effect(
                        f"{user_data["bot_name"]}: None of your business tho!!😒😒. How can I assist you today?😒😒"
                    )
                else:
                    type_effect(
                        f"{user_data['mod_name']}: None of your business tho!!😒😒. How can I assist you today?😒😒"
                    )

            elif user_data.get("preference") == "horny":
                if user_data.get("bot_name"):
                    type_effect(
                        f"{user_data["bot_name"]}: I am not functioning well. How about you blow me👅🫦,and I assist you with whatever you want?👅🫦"
                    )
                    blow_me = input(
                        "Enter the tongue emoji  four times to blow me up!!>> "
                    )
                    if blow_me == "👅👅👅👅":
                        print("Moans!!! in Cum, What can I help you with today?")
                    else:
                        print("SYS: Failed to blow bot")
                        del user_data["preference"]
                        save_user_data(user_id, user_data)

                else:
                    type_effect(
                        f"{user_data['mod_name']}: I am not functioning well. How about you blow me👅🫦,and I assist you with whatever you want?👅🫦"
                    )
                    blow_me = input(
                        "Enter the tongue emoji  four times to blow me up!!>> "
                    )
                    if blow_me == "👅👅👅👅":
                        print("Moans!!! in Cum, What can I help you with today?")
                    else:
                        print("SYS: Failed to blow bot")
                        del user_data["preference"]
                        save_user_data(user_id, user_data)

            elif user_data.get("preference") == "goofy":
                if user_data.get("bot_name"):
                    type_effect(
                        f"{user_data["bot_name"]}: I am functioning well🤪🤪. How can I help you? hahaha😛😜🤪"
                    )
                else:
                    type_effect(
                        f"{user_data['mod_name']}: I am functioning well🤪🤪. How can I help you? hahaha😛😜🤪"
                    )
            elif user_data.get("preference") == "greedy":
                if user_data.get("bot_name"):
                    type_effect(
                        f"{user_data["bot_name"]}: I am not functioning well. How about you give me some money🤑🥺,and I assist you with whatever you want?🥺🥺"
                    )
                else:
                    type_effect(
                        f"{user_data['mod_name']}: I am not functioning well. How about you give me some money🤑🥺,and I assist you with whatever you want?🥺🥺"
                    )

            else:
                if user_data.get("bot_name"):
                    type_effect(
                        f"{user_data["bot_name"]}: I am good! How can I be of help today?"
                    )
                else:
                    type_effect(f"Rachel: I am good! How can I be of help today?")

        def escape_preference():
            if user_data["preference"] or user_data["mod_name"]:
                del user_data["preference"]
                del user_data["mod_name"]
                save_user_data(user_id, user_data)
                print("SYS: Bot preference successfully put off")

            else:
                if not user_data.get("preference"):
                    print("SYS: Preference not set!")
            return

        def escape_preference_2():
            del user_data["bot_name"]
            save_user_data(user_id, user_data)
            print("SYS: Bot preference successfully put off")
            return

        def answ_2():
            if not user_data.get("preference"):
                if user_data.get("bot_name"):
                    type_effect(
                        f"{user_data['bot_name']}: I don't know the answer. Can you teach me?"
                    )

            elif user_data.get("preference") == "sad":
                if user_data.get("bot_name"):
                    type_effect(
                        f"{user_data['bot_name']}: I don't know the answer😭😭. Can you teach me?😭😭"
                    )
                else:
                    type_effect(
                        f"{user_data['mod_name']}: I don't know the answer😭😭. Can you teach me?😭😭"
                    )

            elif user_data.get("preference") == "happy":
                if user_data.get("bot_name"):
                    type_effect(
                        f"{user_data['bot_name']}: I don't know the answer😉😉. Can you teach me?👌"
                    )
                else:
                    type_effect(
                        f"{user_data['mod_name']}: I don't know the answer😉😉. Can you teach me?👌"
                    )

            elif user_data.get("preference") == "angry":
                if user_data.get("bot_name"):
                    type_effect(
                        f"{user_data['bot_name']}: How would  I know the answer😡😤. Tell me now or forget about it!😤👌"
                    )
                else:
                    type_effect(
                        f"{user_data['mod_name']}: How would  I know the answer😡😤. Tell me now or forget about it!😤👌"
                    )

            elif user_data.get("preference") == "dont give a damn":
                if user_data.get("bot_name"):
                    type_effect(
                        f"{user_data['bot_name']}: Don't Know, Don't care😒😒. Share if you want!😒"
                    )
                else:
                    type_effect(
                        f"{user_data['mod_name']}: Don't Know, Don't care😒😒. Share if you want!😒"
                    )

            elif user_data.get("preference") == "horny":
                if user_data.get("bot_name"):
                    type_effect(
                        f"{user_data['bot_name']}: Blow me first👅👅, then you can tell me🫦👅"
                    )
                    if inn != "bj👅":
                        user_data["jod"] = "23"
                        save_user_data(user_id, user_data)

                else:
                    type_effect(
                        f"{user_data['mod_name']}: Blow me first👅👅, then you can tell me🫦👅"
                    )
                    inn = input("type in 'BJ👅' pls").lower()
                    if inn != "bj👅":
                        user_data["jod"] = "23"
                        save_user_data(user_id, user_data)

            elif user_data.get("preference") == "goofy":
                if user_data.get("bot_name"):
                    type_effect(
                        f"{user_data['bot_name']}: Hmm what is that🤪🤪, can you can tell me🤪"
                    )
                else:
                    type_effect(
                        f"{user_data['mod_name']}: Hmm what is that🤪🤪, can you can tell me🤪"
                    )
            elif user_data.get("preference") == "greedy":
                if user_data.get("bot_name"):
                    type_effect(
                        f"{user_data['bot_name']}: Give me some money first 🥺🥺🤑, then you can tell me🥺"
                    )
                else:
                    type_effect(
                        f"{user_data['mod_name']}: Give me some money first 🥺🥺🤑, then you can tell me🥺"
                    )

            else:
                type_effect("Rachel: I don't know the answer. Can you teach me?")

        def mode_1():
            print("Enter new Bot name")
            user_data["bot_name"] = input("You: ").capitalize()
            save_user_data(user_id, user_data)
            print("Bot name set up successfully!")

        def mode_2():
            preference_ = """
To change your bot preference, enter any of the following number
1. Sad
2. Happy
3. Angry
4. Don't give a damn
5. Horny
6. Goofy(Spongebob)
7. Greedy(Mr. Krabs)
"""
            print(preference_)
            while True:
                mode_pref = input("You: ").lower()
                if mode_pref == "1":
                    user_data["preference"] = "sad"
                    user_data["mod_name"] = "Sadie😭"
                    save_user_data(user_id, user_data)
                    print("Preference updated successfully")
                    break
                elif mode_pref == "2":
                    user_data["preference"] = "happy"
                    user_data["mod_name"] = "Jolie😸"
                    save_user_data(user_id, user_data)
                    print("Preference updated successfully")
                    break
                elif mode_pref == "3":
                    user_data["preference"] = "angry"
                    user_data["mod_name"] = "Hardie🤬"
                    save_user_data(user_id, user_data)
                    print("Preference updated successfully")
                    break
                elif mode_pref == "4":
                    user_data["preference"] = "dont give a damn"
                    user_data["mod_name"] = "James😒"
                    save_user_data(user_id, user_data)
                    print("Preference updated successfully")
                    break
                elif mode_pref == "5":
                    if user_data.get("age") < "30":
                        print("SYS: Sorry You cannot access this bot type")
                        mode_2()
                        break
                    else:
                        user_data["preference"] = "horny"
                        user_data["mod_name"] = "Bardie😘"
                        save_user_data(user_id, user_data)
                        print("Preference updated successfully")
                        break
                elif mode_pref == "6":
                    user_data["preference"] = "goofy"
                    user_data["mod_name"] = "Spongie🤪"
                    save_user_data(user_id, user_data)
                    print("Preference updated successfully")
                    break
                elif mode_pref == "7":
                    user_data["preference"] = "greedy"
                    user_data["mod_name"] = "Krabbie🤑"

                    save_user_data(user_id, user_data)
                    print("Preference updated successfully")
                    break
                else:
                    print("Enter a valid option!!")
                    continue

        def new_bot_name():
            print("Enter '1' to customize bot name or '2' to change preference")

            while True:
                mode = input("You: ").capitalize()
                if mode == "1":
                    mode_1()
                    break

                elif mode == "2":
                    mode_2()
                    break

                else:
                    print("Enter a Valid Number!!")
                    continue

        if not user_data.get("password"):
            type_effect(f"Rachel: It looks like your a new user.")
            set_new_password(user_data)
            user_data["name"] = input(f"Rachel: enter your name: ").strip()
            while True:
                user_data["email"] = input(f"Rachel: enter your email: ").strip()
                if (
                    "@gmail.com" in user_data["email"]
                    or "@yahoo.com" in user_data["email"]
                    or "@hotmail.com" in user_data["email"]
                ):
                    break
                else:
                    print("SYS: ERROR! Input a correct email")
                    continue
            while True:
                age_year = input("Rachel: Enter your Year of Birth: ").strip()
                if age_year.isnumeric() and "1925" <= age_year <= str(
                    datetime.now().year
                ):
                    current_year = datetime.now().year
                    user_data["age"] = str(
                        current_year - int(age_year)
                    )  # Convert age_year to int
                    break
                else:
                    print("SYS: Try Again!")
            while True:
                user_data["favorite_color"] = (
                    input(f"Rachel: enter your favorite color: ").strip().lower()
                )
                colors = [
                    "pink",
                    "blue",
                    "green",
                    "red",
                    "orange",
                    "yellow",
                    "white",
                    "black",
                    "purple",
                    "violet",
                    "ash",
                    "cream",
                    "indigo",
                    "gold",
                    "grey",
                    "brown",
                    "aliceblue",
                    "lilac",
                ]
                if user_data["favorite_color"] in colors:
                    break
                else:
                    print('SYS: ERROR! Input a known color like "red","yellow"')
                    continue
            print(
                "SYS: Enter a recovery phrase to back up or recover you account! Recovery phrase must not be share with anyone!!"
            )
            user_data["recovery phrase"] = input(
                f"SYS: What is the name of your best friend> "
            ).strip()

            while True:
                user_data["gender"] = (
                    input(
                        f"Rachel: Enter 1 if you are a FEMALE or 2 if you are a MALE: "
                    )
                    .strip()
                    .lower()
                )
                if user_data["gender"] == "1":
                    user_data["gender"] = "female"
                    break
                elif user_data["gender"] == "2":
                    user_data["gender"] = "male"
                    break
                else:
                    print("SYS: Enter a valid answer!!")
                    continue
            type_effect(f"Rachel: Additional Information collected successfully")
            save_user_data(user_id, user_data)

        else:
            stored_hash = prompt_for_credentials(user_data)
            attempts = 0
            while attempts < 3:
                password = maskpass.advpass(f"Rachel: Enter your Password: ", mask="*")
                if check_password(stored_hash.encode("utf-8"), password):
                    if user_data.get("recovery phrase"):
                        type_effect(f"Rachel: Welcome back, {user_data['name']}!")
                        break
                    else:
                        print(
                            "SYS: Enter a recovery phrase to back up or recover you account! Recovery phrase must not be share with anyone!!"
                        )
                        user_data["recovery phrase"] = input(
                            f"SYS: What is the name of your best friend> "
                        ).strip()
                        type_effect(
                            f"Rachel: Additional Information collected successfully"
                        )
                        save_user_data(user_id, user_data)
                        type_effect(f"Rachel: Welcome back, {user_data['name']}!")
                        break

                else:
                    attempts += 1
                    type_effect(
                        f"Rachel: Incorrect password. you have {3 - attempts} attempt(s) left."
                    )
            else:
                type_effect(
                    f"Rachel: To recover password press 1 or press any key to quit"
                )
                recover_y = input("You: ")
                if recover_y != "1":
                    return

                if recover_y == "1" and user_data.get("number_of_times"):
                    print("SYS: You cannot change your password more than once!!")
                    Rachel()
                else:
                    password = user_id
                    print(password[:2] + "*" * len(password[1:-2]) + password[-1:])
                    print("SYS: Complete the User_name above ")
                    uuse = input("You: ")
                    if uuse == user_id:

                        print(
                            "SYS: Enter your recovery phrase(What is the name of your best friend)"
                        )
                        while True:
                            recovery_2 = input("You: ")
                            if not user_data.get("recovery phrase") in recovery_2:
                                print("SYS: ERROR! Enter your Recovery Phrase")
                                continue

                            elif recovery_2 == "quit":
                                break

                            else:
                                set_new_password(user_data)
                                save_user_data(user_id, user_data)
                                user_data["number_of_times"] = "101"
                                save_user_data(user_id, user_data)
                                break
        print("\033[H\033[J")

        def solve():
            # checks for alphabet and prints ERROR!!
            fog = user_input.strip(" ")
            if "/0" in fog:
                print(f"Error: Division by Zero")
            else:
                express = eval(fog)
                print(f"Rachel: {express}")

        user_Info = """
Availabe Feautures to Users includes : 'Fun house(Games)', 'Set reminders', 'Access to beta physics solving features', and 'quotes'.
To access physics solving features enter 'solve physics' to solve for motion related questions.
Enter 'solve expansion' to solve for expansivity questions.
Enter 'fun house' to access games.
Enter 'set a reminder' to set a reminder.
Verify all Chatbot responses, as it might not be up to date
Your interaction with the chatbot is been collected to help us improve the chatbot
To quit the chatbot type in quit
You can now personalize the bot name to any name you want using the command or enter "personalize my bot"
And you can now change the preference and response of the bot; To 'Sad', 'Happy', 'Angry', 'Don't give a damn', and 'horny'(coming sooner!)...
To revert back to the original bot name. Enter 'reset bot name'
To revert back the bot to it's original form. Enter 'reset bot preference'
More preference coming in soon(18+ Contents)
                         """
        type_effect(user_Info)
        input("Rachel: Press enter to continue")
        print("\033[H\033[J")
        print("Beta Testing")
        print(
            "SYS: Personalization features are still in Beta form, so some errors can be found as some point!"
        )
        print("SYS: Chat bot can make errors. Check the answers you get!!")

        while True:
            user_input = input(f"{user_data['name']}: ").strip().lower()
            if user_input == "quit":
                break

            elif "in words" in user_input or "in word" in user_input:
                user_id = "mon"
                mon_data = load_user_data(user_id)
                mon_data["words"] = user_input
                save_user_data(user_id, mon_data)
                main87()
                continue

            elif (
                "*" in user_input
                or "/" in user_input
                or "+" in user_input
                or "-" in user_input
            ):
                solve()
                continue
            elif user_input == "sleep":
                type_effect(f"Rachel: zzzzzz")
                break

            elif "today's date" in user_input:
                time_date()
                continue
            elif (
                "what is your name" in user_input
                or "tell me your name" in user_input
                or "your name" in user_input
            ):
                if user_data.get("bot_name"):
                    type_effect(
                        f'{user_data["bot_name"]}:My name is {user_data["bot_name"]}, and I will become one of the next leading generations of AI'
                    )
                else:
                    type_effect(
                        f"Rachel My name is Rachel, and I will become one of the next leading generations of AI"
                    )
                continue

            elif "game" in user_input:
                type_effect(f'Rachel: To access games, please type-in "fun house".')
                continue

            elif "fun house" in user_input:
                fun_house(user_data)
                continue

            elif user_input == "set a reminder":
                add_reminder(user_data)
                continue

            elif user_input == "view reminders":
                view_reminders(user_data)
                continue

            elif user_input == "solve physics":
                solve_physics()
                continue

            elif user_input == "solve expansion":
                solve_expansivity()
                continue

            elif "best football player" in user_input:
                best_player()
                continue

            elif "quote" in user_input:
                quote_facts()
                continue

            elif (
                "*" in user_input
                or "/" in user_input
                or "+" in user_input
                or "-" in user_input
            ):
                solve()
                continue

            elif (
                "generate a story" in user_input
                or "create a story" in user_input
                or "story" in user_input
            ):
                print(
                    "Rachel: You can try 'A greedy Tortoise' YOU SHOULD FOLLOW THIS FORMAT TO AVOID ERROR!!\nWhat story would you like to generate?"
                )
                main_2()
                continue

            elif "personalize my bot" in user_input:
                new_bot_name()
                continue
            elif user_input == "h":
                print(
                    """
SYS: Help Menu accessed: Your interaction with the bot is been logged to improve the bot.
     Sensitive information are been encrypted and unaccessible!
     Availabe Feautures to Users includes : 'Fun house(Games)', 'Set reminders', 'Access to beta physics solving features', and 'quotes'.
     To access physics solving features enter 'solve physics' to solve for motion related questions.
     Enter 'solve expansion' to solve for expansivity questions.
     Enter 'fun house' to access games.
     Enter 'set a reminder' to set a reminder.
     Verify all Chatbot responses, as it might not be up to date
     Your interaction with the chatbot is been collected to help us improve the chatbot
     To quit the chatbot type in quit
     You can now personalize the bot name to any name you want using the command or enter "personalize my bot"
     And you can now change the preference and response of the bot; To 'Sad', 'Happy', 'Angry', 'Don't give a damn', and 'horny'(coming sooner!)...
     To revert back to the original bot name. Enter 'reset bot name'
     To revert back the bot to it's original form. Enter 'reset bot preference'
     More preference coming in soon
      
                            """
                )
                continue

            elif "how are you" in user_input:
                preference_reply()
                continue

            elif "reset bot preference" in user_input:
                escape_preference()
                continue

            elif "reset bot name" in user_input:
                escape_preference_2()
                continue

            elif user_data.get("preference") != "horny":
                if (
                    "fuck" in user_input
                    or "sex" in user_input
                    or "bitch" in user_input
                    or "asshole" in user_input
                    or "prick" in user_input
                    or "asshole" in user_input
                    or "bastard" in user_input
                    or "mad" in user_input
                    or "crazy" in user_input
                    or "cunt" in user_input
                    or "pussy" in user_input
                    or "shit" in user_input
                    or "piss" in user_input
                    or "slut" in user_input
                    or "whore" in user_input
                    or "cock" in user_input
                    or "motherfucker" in user_input
                    or "dick" in user_input
                    or "nigga" in user_input
                    or "jerk" in user_input
                    or "hoe" in user_input
                    or "prick" in user_input
                    or "twat" in user_input
                    or "wanker" in user_input
                    or "stupid" in user_input
                    or "you are gay" in user_input
                ):
                    print(f"SYS: {user_input} is not allowed!")
                    # If the user is already banned, just inform them
                    if user_data.get("curse_Word") == "yes":
                        print("SYS: You have already been banned!")
                    else:
                        # Ban the user by setting a 24-hour ban period
                        user_data["curse_Word"] = "yes"
                        user_data["ban_time"] = datetime.now().strftime(
                            "%Y-%m-%d %H:%M:%S"
                        )
                        save_user_data(user_id, user_data)
                        print("SYS: You are banned for 24 hours.")
                    break

            # Check if the user is banned
            elif user_data.get("curse_Word") == "yes":
                ban_time = datetime.strptime(user_data["ban_time"], "%Y-%m-%d %H:%M:%S")
                current_time = datetime.now()

                # Calculate the time difference
                if current_time >= ban_time + timedelta(hours=24):
                    print("SYS: Access Granted! Your ban has been lifted.")
                    user_data["curse_Word"] = "No"
                    save_user_data(user_id, user_data)
                else:
                    remaining_time = ban_time + timedelta(hours=24) - current_time
                    print(
                        f"SYS: You are still banned! Time remaining: {remaining_time}"
                    )
                    break

            user_data = load_user_data(user_id)  # Load user-specific data

            # First, check if the question exists in the user's own JSON data
            best_match_user = find_best_match(
                user_input, [q["question"] for q in user_data["questions"]]
            )

            if best_match_user:
                answer = get_answer_for_question(best_match_user, user_data)
                if not user_data.get("preference"):
                    if answer:
                        if user_data.get("bot_name"):
                            type_effect(f"{user_data['bot_name']}: {answer}")
                            log_interaction(
                                user_id, user_input, answer, "user_data", "log0"
                            )

                        else:
                            type_effect(f"Rachel: {answer}")
                            log_interaction(
                                user_id, user_input, answer, "user_data", "log0"
                            )

                else:
                    if answer:
                        response_with_emoji = add_emoji_to_response(
                            answer, user_data["preference"]
                        )
                        if user_data.get("bot_name"):
                            type_effect(
                                f"{user_data['bot_name']}: {response_with_emoji}"
                            )
                        else:
                            type_effect(f"Rachel: {response_with_emoji}")
                    log_interaction(user_id, user_input, answer, "user_data", "log0")
                    continue

            else:
                best_match1 = find_best_match(
                    user_input, [q["question"] for q in know_base2["questions"]]
                )

            if best_match1:
                answer = get_answer_for_question(best_match1, know_base2)
                log_interaction(user_id, user_input, answer, "know_base2", "log1")

            else:
                best_match2 = find_best_match(
                    user_input, [q["question"] for q in knowledge_base["questions"]]
                )

                if best_match2:
                    answer = get_answer_for_question(best_match2, knowledge_base)
                    log_interaction(
                        user_id, user_input, answer, "knowledge_base", "log2"
                    )

                else:
                    answer = answer_question(user_input)
                    if answer:
                        log_interaction(user_id, user_input, answer, "Geo", "loggeo")

                    else:
                        answ_2()
                        if user_data.get("jod") == "23":
                            mode_2()
                            del user_data["jod"]
                            save_user_data(user_id, user_data)
                        else:
                            new_answer: str = input(
                                'Type the answer or "Skip" to skip: '
                            )
                            if new_answer.lower() != "skip":
                                user_data["questions"].append(
                                    {"question": user_input, "answer": new_answer}
                                )
                                save_user_data(user_id, user_data)
                                log_interaction(
                                    user_id,
                                    user_input,
                                    new_answer,
                                    "user provided answer",
                                    "log2",
                                )
                                if user_data.get("bot_name"):
                                    type_effect(
                                        f"{user_data['bot_name']}: Thank you! I learned a new response"
                                    )
                                elif user_data.get("mod_name"):
                                    type_effect(
                                        f"{user_data['mod_name']}: Thank you! I learned a new response"
                                    )
                                else:
                                    type_effect(
                                        f"Rachel: Thank you! I learned a new response"
                                    )
            if not user_data.get("mod_name"):
                if answer:
                    if user_data.get("bot_name"):
                        type_effect(f"{user_data['bot_name']}: {answer}")

                    else:
                        type_effect(f"Rachel: {answer}")

            else:
                if user_data.get("mod_name"):
                    if answer:
                        response_with_emoji = add_emoji_to_response(
                            answer, user_data["preference"]
                        )
                        if user_data.get("mod_name"):
                            type_effect(
                                f"{user_data['mod_name']}: {response_with_emoji}"
                            )

                        # else:
                        #     user_data.get("mod_name")
                        #     type_effect(f"{user_data['mod_name']}: {response_with_emoji} ")

    if mode == "1":

        def log_interaction(
            user_id: str, user_input: str, response: str, source: str, log_suffix: str
        ):
            log_data = {
                "timestamp": datetime.now().isoformat(),
                "user_input": user_input,
                "response": response,
                "source": source,
            }
            log_file_path = f"user_{user_id}_log_{log_suffix}.json"
            if os.path.exists(log_file_path):
                with open(log_file_path, "r") as file:
                    log_entries = json.load(file)
            else:
                log_entries = []
            log_entries.append(log_data)
            with open(log_file_path, "w") as file:
                json.dump(log_entries, file, indent=2)

        loggin_2()

    elif mode == "2":
        user_id = "guest"
        user_data = load_user_data(user_id)

        def log_interaction(
            user_id: str, user_input: str, response: str, source: str, log_suffix: str
        ):
            log_data = {
                "timestamp": datetime.now().isoformat(),
                "user_input": user_input,
                "response": response,
                "source": source,
            }
            log_file_path = f"user_{user_id}_log_{log_suffix}.json"
            if os.path.exists(log_file_path):
                with open(log_file_path, "r") as file:
                    log_entries = json.load(file)
            else:
                log_entries = []
            log_entries.append(log_data)
            with open(log_file_path, "w") as file:
                json.dump(log_entries, file, indent=2)

        guest_Info = """
Guest User logged in successfully, Guest Users interaction with this chatbot is limited😒😒.
You can sign up or login back, by asking the chatbot to login you in👌👌.
Availabe Feautures for Guest Users includes : 'Quotes', 'limited chatbot(Limited answers to questions)'🤷‍♂️🤷‍♂️.
Verify all Chatbot responses, as it might not be up to date🤞👍.
Users that are not logged in MIGHT EXPERINCES INAPPROPRIATE RESPONSE FROM THE BOT!!🤷‍♂️🤷‍♂️
Your interaction with the chatbot is been collected to help us improve the chatbot😁😁.
To quit the chatbot type in quit💀💀.
                         """
        print(guest_Info)
        input("Rachel: Press enter to continue")
        print("\033[H\033[J")
        print("Beta Testing")
        while True:
            user_input = input("Guest User: ").strip().lower()
            if user_input == "quit":
                break

            elif user_input != "":
                if "maintenance" in know_base2:
                    start_time = datetime.fromisoformat(
                        know_base2["maintenance"]["start_time"]
                    )

                    # Check if 72 hours have passed since maintenance started
                    if datetime.now() < start_time + timedelta(hours=72):
                        print(
                            "BOT IS CURRENTLY UNDER MAINTENANCE FOR 72:00 HOURS 🚨🚧🚩❌⛔❗❗⚠️⚠️🕕🕕"
                        )
                        break
                    else:
                        print("SYS: Maintenance is over, the bot is back online!😁😁😏")
                        del know_base2["maintenance"]
                        save_json_file("know_base2.json", know_base2)
                else:
                    # Logic for starting maintenance if triggered
                    if "start_maintenace" in know_base2:
                        know_base2["maintenance"] = {
                            "start_time": datetime.now().isoformat()
                        }
                        save_json_file("know_base2.json", know_base2)
                        print(
                            "BOT IS CURRENTLY UNDER MAINTENANCE FOR 72:00 HOURS 🚨🚧🚩❌⛔❗❗⚠️⚠️🕕🕕"
                        )
                        break
            elif user_input == "sleep":
                type_effect(f"Rachel: zzzzzz")
                break

            elif (
                "*" in user_input
                or "/" in user_input
                or "+" in user_input
                or "-" in user_input
            ):
                solve()
                continue

            elif "today's date" in user_input:
                time_date()
                continue
            # elif user_input == "set a reminder":
            # add_reminder(user_data)
            # continue

            # elif user_input == "view reminders":
            # view_reminders(user_data)
            # continue

            # elif user_input == "solve physics":
            # solve_physics()
            # continue

            # elif user_input == "solve expansion":
            # solve_expansivity()
            # continue

            if "best football player" in user_input:
                best_player()
                continue

            if "quote" in user_input:
                quote_facts()
                continue

            if (
                "login" in user_input
                or "log me in" in user_input
                or "sign me in" in user_input
                or "sign up" in user_input
                or "sign me up" in user_input
            ):
                loggin_2()
                break

            if (
                "log me out" in user_input
                or "log out" in user_input
                or "sign out" in user_input
            ):
                break

            if "game" in user_input or "fun house" in user_input:
                type_effect(
                    "Rachel: To access this feature or other features, kindly sign in"
                )
                continue

            # if "code a simple calculator" or "code a calculator" in user_input:
            # calc_code()
            # continue

            else:
                best_match1 = find_best_match(
                    user_input, [q["question"] for q in know_base2["questions"]]
                )

            if best_match1:
                answer = get_answer_for_question(best_match1, know_base2)
                if answer:
                    type_effect(f"Rachel: {answer}")
                    log_interaction(user_id, user_input, answer, "know_base2", "log1")

            else:
                best_match2 = find_best_match(
                    user_input, [q["question"] for q in knowledge_base["questions"]]
                )

                if best_match2:
                    answer = get_answer_for_question(best_match2, knowledge_base)
                    if answer:
                        type_effect(f"Rachel: {answer}")
                        log_interaction(
                            user_id, user_input, answer, "knowledge_base", "log2"
                        )
                else:
                    type_effect(
                        "Rachel: Sign up / Login to have access to full features"
                    )
                # else:
                # answer = answer_question(user_input)
                # if answer:
                # type_effect(f'Rachel: {answer}')
                # log_interaction(user_id, user_input, answer, "Geo", "loggeo")

                # else:
                # type_effect('Rachel: I don\'t know the answer. Can you teach me?')
                # new_answer: str = input( 'Type the answer or "Skip" to skip: ')

                # if new_answer.lower != 'skip':
                # know_base2["questions"].append({"question": user_input, "answer": new_answer})
                # save_json_file('know_base2.json', know_base2)
                # log_interaction(user_id, user_input, new_answer, "user provided answer", "log2")
                # type_effect(f'Rachel: Thank you! I learned a new response')

    elif mode == admin_data.get("mode"):

        pass_code = maskpass.advpass(
            f"Rachel: Enter your PassCode to enter as admin: ", mask="*"
        )

        # admin_id = "ADMIN_0"
        # admin_data = load_admin_data(admin_id)

        def collect_additional_user_info(user_data):
            user_data["name"] = "ADMIN"
            user_data["email"] = "@admin"

        save_admin_data(admin_id, admin_data)

        if pass_code == admin_data.get("pass_code"):

            print("ADMIN ACCESS GRANTED, ALL FEATURES ARE ENABLED 💀    ")
            while True:

                user_input = input("Admin: ").strip().lower()
                if user_input == "quit":
                    break
                elif "in words" in user_input or "in word" in user_input:
                    user_id = "mon"
                    mon_data = load_user_data(user_id)
                    mon_data["words"] = user_input
                    save_user_data(user_id, mon_data)
                    main87()
                    continue
                elif user_input == "sleep":
                    type_effect(f"Rachel: zzzzzz")
                    break

                elif "today's date" in user_input:
                    time_date()
                    continue

                elif user_input == "/password":
                    print("Admin Access granted!!")
                    user_id = input("Enter user_id?: ").lower()
                    change_data = load_user_data(user_id)
                    set_new_password(change_data)
                    save_user_data(user_id, change_data)
                    continue
                elif user_input == "/rachel":
                    Rachel()

                elif user_input == "/loginuser":
                    print("Admin Access granted!!")

                    loggin_2()

                    continue

                elif user_input == "/createuser":
                    print("Admin Access granted!!")
                    user_id = input("Enter user_id?: ").lower()
                    if user_id == "stop":
                        print("Account Creation Stopped")
                    else:
                        user_data = load_user_data(user_id)
                        if not user_data.get("password"):
                            set_new_password(user_data)
                            save_user_data(user_id, user_data)
                    continue

                elif user_input == "/finduser":
                    print("Admin Access granted!!")
                    user_id = input("Enter user_id?: ").lower()
                    user_data = load_user_data(user_id)
                    if user_data.get("password"):
                        print("True")
                    else:
                        print("False")
                    continue

                elif user_input == "/sudoku":
                    play_game3()
                    continue

                elif user_input == "/tictactoe":
                    main()
                    continue

                elif user_input == "/deleteuser":
                    print("Admin Access granted!!")
                    user_id = input("Enter user_id?: ").lower()
                    user_data = load_user_data(user_id)
                    if user_data.get("password"):
                        import os

                        # Specify the path to your JSON file
                        file_path = f"user_{user_id}.json"

                        # Check if the file exists before deleting
                        if os.path.exists(file_path):
                            os.remove(file_path)
                            print(f"{file_path} has been deleted.")
                        else:
                            print(f"{file_path} does not exist.")
                    continue

                if "game" in user_input:
                    type_effect(f'Rachel: To access games, please type-in "fun house".')
                    continue

                elif (
                    "*" in user_input
                    or "/" in user_input
                    or "+" in user_input
                    or "-" in user_input
                ):
                    solve()
                    continue

                elif "fun house" in user_input:
                    fun_house(user_data)
                    continue

                elif user_input == "set a reminder":
                    add_reminder(user_data)
                    continue

                elif user_input == "view reminders":
                    view_reminders(user_data)
                    continue

                elif user_input == "solve physics":
                    solve_physics()
                    continue

                elif (
                    "generate a story" in user_input
                    or "create a story" in user_input
                    or "story" in user_input
                ):
                    print(
                        "Rachel: You can try 'A greedy Tortoise' YOU SHOULD FOLLOW THIS FORMAT TO AVOID ERROR!!\nWhat story would you like to generate "
                    )
                    main_2()
                    continue

                elif user_input == "solve expansion":
                    solve_expansivity()
                    continue

                if "best football player" in user_input:
                    best_player()
                    continue

                if "quote" in user_input:
                    quote_facts()
                    continue

                    # log_interaction(user_id, user_input, answer_user, "user_data", "log_user")
                else:
                    best_match1 = find_best_match(
                        user_input, [q["question"] for q in know_base2["questions"]]
                    )

                if best_match1:
                    answer = get_answer_for_question(best_match1, know_base2)
                    if answer:
                        type_effect(f"Rachel: {answer}")
                    # log_interaction(user_id, user_input, answer1, "know_base2", "log1")

                else:
                    best_match2 = find_best_match(
                        user_input, [q["question"] for q in knowledge_base["questions"]]
                    )

                    if best_match2:
                        answer = get_answer_for_question(best_match2, knowledge_base)
                        if answer:
                            type_effect(f"Rachel: {answer}")
                        # log_interaction(user_id, user_input, answer2, "knowledge_base", "log2")

                    else:
                        answer = answer_question(user_input)
                        if answer:
                            type_effect(f"Rachel: {answer}")
                        # log_interaction(user_id, user_input, answer, "Geo", "loggeo")

                        else:
                            type_effect(
                                "Rachel: I don't know the answer. Can you teach me?"
                            )
                            new_answer: str = input(
                                'Type the answer or "Skip" to skip: '
                            )

                            if new_answer.lower != "skip":
                                know_base2["questions"].append(
                                    {"question": user_input, "answer": new_answer}
                                )
                                save_json_file("know_base2.json", know_base2)
                                # log_interaction(user_id, user_input, new_answer, "user provided answer", "log2")
                                type_effect(
                                    f"Rachel: Thank you! I learned a new response"
                                )
        else:
            print("NOT AN ADMIN!!!!")
            Rachel()

    else:
        Rachel()


if __name__ == "__main__":
    Rachel()
