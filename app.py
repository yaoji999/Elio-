from flask import Flask, render_template, request, session, redirect, url_for
import json

app = Flask(__name__)
app.secret_key = "elio_super_secret_key"

# Correction ici : il faut charger les données JSON !
with open('ELIO_Plan_92_Jours_Complet_Calories.json', 'r', encoding='utf-8') as f:
    all_plans = json.load(f)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        session['age'] = int(request.form['age'])
        session['taille'] = int(request.form['taille'])
        session['poids'] = int(request.form['poids'])
        session['objectif'] = request.form['objectif']
        session['niveau'] = request.form['niveau']
        session['jours'] = int(request.form['jours'])
        session['regime'] = request.form['regime']
        session['week'] = 0
        return redirect(url_for('results'))
    return render_template('elio_formulaire.html')

@app.route('/results', methods=['GET', 'POST'])
def results():
    if 'week' not in session:
        return redirect(url_for('index'))

    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'next':
            session['week'] = min(session['week'] + 1, (session['jours'] - 1) // 7)
        elif action == 'prev':
            session['week'] = max(session['week'] - 1, 0)

    start = session['week'] * 7
    end = min(start + 7, session['jours'])
    plan_data = {f"Jour {i+1}": all_plans[i] for i in range(start, end)}

    return render_template("results_calories.html",
                           age=session['age'],
                           taille=session['taille'],
                           poids=session['poids'],
                           objectif=session['objectif'],
                           niveau=session['niveau'],
                           regime=session['regime'],
                           jours=session['jours'],
                           plan_data=plan_data,
                           semaine=session['week'] + 1,
                           total_semaines=(session['jours'] - 1) // 7 + 1)

if __name__ == '__main__':
    app.run(debug=True)
