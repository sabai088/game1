from flask import Flask, render_template
import random

app = Flask(__name__)

@app.route('/')
def index():
    # Generate a random number from 0 to 1 (0 - heads, 1 - tails)
    result = random.randint(0, 1)
    # Determine the result of the coin toss
    coin_side = "Heads" if result == 0 else "Tails"
    # Pass the result to the HTML template
    return render_template('index.html', coin_side=coin_side)

if __name__ == '__main__':
    app.run(debug=True)
