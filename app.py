from flask import Flask, render_template, request
import json

app = Flask(__name__)

# Charger le fichier JSON des 90 jours
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

        # Filtres selon les régimes alimentaires
        if regime in ["halal", "végétarien", "végan"]:
            replacements = {
                "halal": {
                    "porc": "poulet grillé",
                    "bacon": "œufs brouillés",
                    "jambon": "poisson vapeur",
                    "saucisse": "steak haché halal",
                    "lard": "falafel maison",
                    "alcool": "jus de grenade"
                },
                "végétarien": {
                    "steak": "galette de lentilles",
                    "poulet": "tofu mariné",
                    "thon": "falafel",
                    "jambon": "œuf dur",
                    "poisson": "burger végétal"
                },
                "végan": {
                    "fromage": "tofu fumé",
                    "œuf": "tofu brouillé",
                    "yaourt": "yaourt soja",
                    "lait": "lait d'amande",
                    "beurre": "huile d'olive",
                    "poulet": "pois chiches rôtis",
                    "poisson": "steak végétal"
                }
            }

            def adapter_texte(texte, regime):
                texte_modif = texte
                for interdit, remplacement in replacements[regime].items():
                    texte_modif = texte_modif.replace(interdit, remplacement)
                    texte_modif = texte_modif.replace(interdit.capitalize(), remplacement)
                return texte_modif

            for plan in all_plans:
                for repas in ["petit_dejeuner", "dejeuner", "diner"]:
                    plan[repas]["desc"] = adapter_texte(plan[repas]["desc"], regime)

        # Sélectionner le nombre de jours demandés
        plan_data = {}
        for i in range(1, jours + 1):
            plan_data[f"Jour {i}"] = all_plans[i - 1]

        return render_template("results_calories.html",
                               age=age, taille=taille, poids=poids,
                               objectif=objectif, niveau=niveau,
                               regime=regime, jours=jours,
                               plan_data=plan_data)
    except Exception as e:
        return f"Erreur : {e}"

if __name__ == '__main__':
    app.run(debug=True)
