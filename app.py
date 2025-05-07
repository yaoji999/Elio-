from flask import Flask, render_template, request
import json

app = Flask(__name__)

# Charger les données du fichier JSON
with open('ELIO_Plan_90_Jours_Complet.json', 'r', encoding='utf-8') as f:
    all_plans = json.load(f)

@app.route('/')
def index():
    return render_template('elio_formulaire.html')

@app.route('/generate', methods=['POST'])
def generate():
    try:
        age = int(request.form['age'])
        taille = int(request.form['taille'])
        poids = int(request.form['poids'])
        objectif = request.form['objectif']
        niveau = request.form['niveau']
        jours = int(request.form['jours'])
        regime = request.form['regime']

        # Préparer les jours personnalisés
        plan_data = {}
        for i in range(1, jours + 1):
            jour_plan = all_plans[i - 1]
            plan_data[f"Jour {i}"] = {
                "petit_dejeuner": jour_plan["petit_dejeuner"],
                "dejeuner": jour_plan["dejeuner"],
                "diner": jour_plan["diner"],
                "exercices": jour_plan["exercices"]
            }

        return render_template("results_calories.html",
                               age=age, taille=taille, poids=poids,
                               objectif=objectif, niveau=niveau,
                               regime=regime, jours=jours,
                               plan_data=plan_data)
    except Exception as e:
        return f"Erreur : {e}"

if __name__ == '__main__':
    app.run(debug=True)
