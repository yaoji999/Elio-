from flask import Flask, render_template, request
import json

app = Flask(__name__)

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

        # Charger les 12 semaines depuis le fichier JSON
        with open('ELIO_12_Semaines.json', 'r', encoding='utf-8') as f:
            all_weeks = json.load(f)['plans']

        # Créer le plan final avec rotation sur 12 semaines
        plan_data = {}
        jour_total = 1
        for i in range(jours):
            semaine_index = (i // 7) % 12 + 1
            jour_semaine = i % 7
            semaine_cle = f"Semaine_{semaine_index}"
            jour_plan = all_weeks[semaine_cle][jour_semaine]
            plan_data[f"Jour {jour_total}"] = jour_plan
            jour_total += 1

        return render_template("results_calories.html",
                               age=age, taille=taille, poids=poids,
                               objectif=objectif, niveau=niveau,
                               regime=regime, jours=jours,
                               plan_data=plan_data)
    except Exception as e:
        return f"Erreur : {e}"

if __name__ == '__main__':
    app.run(debug=True)
