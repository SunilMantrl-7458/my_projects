from flask import Flask, render_template
import logging

app = Flask(__name__)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/app.log'),
        logging.StreamHandler()
    ]
)

@app.route('/')
def index():
    return "Telegram Group Analytics Dashboard"

if __name__ == '__main__':
    app.run(debug=True)