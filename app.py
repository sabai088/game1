import random
from math import ceil, log2
from subprocess import run
from flask import Flask, render_template, request

# URL репозитория с рандомайзером
RANDOMIZER_REPO_URL = "https://github.com/sabai088/random"

# Диапазон загадываемого числа
MIN_NUMBER = 1
MAX_NUMBER = 100

# Максимальное количество попыток
MAX_ATTEMPTS = ceil(log2(MAX_NUMBER - MIN_NUMBER + 1))

# Словарь с подсказками
HINTS = {
  "too_low": "The number is higher.",
  "too_high": "The number is lower.",
  "repeat": "You have already entered this number.",
  "invalid": "Enter a number between {} and {}.".format(MIN_NUMBER, MAX_NUMBER)
}

def get_random_value(repo_url):
  """
  Функция для получения случайного значения из репозитория.

  Args:
    repo_url: URL репозитория с рандомайзером.

  Returns:
    Случайное значение.
  """

  # Клонируем репозиторий
  random.seed()
  clone_dir = f".tmp_randomizer_{random.randint(1000, 9999)}"
  run(["git", "clone", repo_url, clone_dir])

  # Получаем случайное значение из файла
  with open(f"{clone_dir}/random_value.txt", "r") as f:
    random_value = f.read().strip()

  # Удаляем клон репозитория
  run(["rm", "-rf", clone_dir])

  return random_value

def generate_random_number():
  return int(get_random_value(RANDOMIZER_REPO_URL))

def is_valid_number(number):
  return MIN_NUMBER <= number <= MAX_NUMBER

def play_game(mode, number=None):
  # Генерация загадываемого числа
  if mode == "single":
    number = generate_random_number()

  # История введенных чисел
  guessed_numbers = set()

  # Цикл попыток
  for attempt in range(1, MAX_ATTEMPTS + 1):
    # Ввод числа
    if mode == "single":
      guess = int(request.form.get("guess"))
    elif mode == "multiplayer":
      # TODO: Implement multiplayer mode
      pass

    # Проверка введенного числа
    if not is_valid_number(guess):
      message = HINTS["invalid"]
      continue

    # Проверка на повтор
    if guess in guessed_numbers:
      message = HINTS["repeat"]
      continue

    # Добавление числа в историю
    guessed_numbers.add(guess)

    # Сравнение с загадываемым числом
    if guess < number:
      message = HINTS["too_low"]
    elif guess > number:
      message = HINTS["too_high"]
    else:
      # Угадали!
      message = f"Congratulations! You guessed the number in {attempt} attempts."
      break

  # Не угадали :(
  if attempt == MAX_ATTEMPTS:
    message = f"You couldn't guess the number. The number was {number}."

  return message

app = Flask(__name__)

@app.route("/")
def index():
  return render_template("index.html")

@app.route("/play", methods=["POST"])
def play():
  mode = request.form.get("mode")
  number = None

  if mode == "single":
    # Single player mode
    message = play_game(mode)
  elif mode == "multiplayer":
    # Multiplayer mode
    # TODO: Implement multiplayer mode
    pass

  return render_template("play.html", message=message)
