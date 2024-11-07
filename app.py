from flask import Flask, render_template


app = Flask(__name__)



@app.route('/')
def question():
    return render_template('question.html')


