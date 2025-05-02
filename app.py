from flask import Flask, render_template, request
import os
import json

app = Flask(__name__)

# Charger les 92 jours depuis le fichier JSON
with open("ELIO_Plan_92_Jours.json", "r", encoding="utf-8") as f:
    all_plans = json.load(f)

@app.route('/')
def home():
    return render_template('elio_formulaire.html')

@app.route('/generate', methods=['POST'])
def generate():
    age = request.form.get('age')
    height = request.form.get('height')
    weight = request.form.get('weight')
    goal = request.form.get('goal')
    level = request.form.get('level')
    days = int(request.form.get('days'))
    diet = request.form.get('diet')

    # Sélection des premiers "jours" en fonction du nombre de jours choisis
    selected_plans = all_plans[:days]

    return render_template("results.html", age=age, height=height, weight=weight,
                           goal=goal, level=level, days=days, diet=diet,
                           plans=selected_plans)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
