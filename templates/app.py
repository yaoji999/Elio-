from flask import Flask, render_template, request
import os

app = Flask(__name__)

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
    days = request.form.get('days')
    diet = request.form.get('diet')

    sport_program = [
        "Échauffement : 10 min de marche rapide ou corde à sauter",
        "Exercice 1 : Squats – 3 séries de 15 reps",
        "Exercice 2 : Pompes – 3 x 10 (sur genoux si débutant)",
        "Exercice 3 : Fentes avant – 3 x 12 reps par jambe",
        "Exercice 4 : Gainage – 3 x 30 sec",
        "Exercice 5 : Crunchs abdos – 3 x 20"
    ]

    meals = {
        "matin": "Porridge avoine + banane + beurre de cacahuète",
        "midi": "Poulet / tofu + riz complet + légumes verts",
        "soir": "Omelette + salade + lentilles / patate douce"
    }

    return render_template("results.html", age=age, height=height, weight=weight,
                           goal=goal, level=level, days=days, diet=diet,
                           sport_program=sport_program, meals=meals)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
