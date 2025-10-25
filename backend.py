from flask import Flask, request, jsonify, send_from_directory
from sympy import symbols, Eq, solve, sympify
import os

app = Flask(__name__, static_folder='static')

@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

@app.route('/about.html')
def about():
    return send_from_directory('static', 'about.html')

@app.route('/style.css')
def style():
    return send_from_directory('static', 'style.css')

@app.route('/solve', methods=['POST'])
def solve_equation():
    data = request.get_json()
    question = data.get('question', '')
    try:
        if "=" in question:
            left, right = question.split("=")
            x = symbols("x")
            eq = Eq(sympify(left), sympify(right))
            solution = solve(eq)
        else:
            solution = sympify(question).evalf()
        return jsonify({"solution": str(solution), "steps": "تم حل المسألة بنجاح ✅"})
    except Exception as e:
        return jsonify({"solution": "خطأ في الحل", "steps": str(e)})

@app.route('/contact', methods=['POST'])
def contact():
    data = request.get_json()
    name = data.get('name', 'مجهول')
    message = data.get('message', '')
    with open('messages.txt', 'a', encoding='utf-8') as f:
        f.write(f"{name}: {message}\n")
    return jsonify({"status": "success"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
