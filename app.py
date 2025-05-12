from flask import Flask, render_template, request, session, redirect, url_for, make_response
import json
from xhtml2pdf import pisa
from io import BytesIO
from flask import render_template_string

app = Flask(__name__)
app.secret_key = "elio_super_secret_key"

# Charger le fichier JSON 92 jours
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

# AJOUT DU TÉLÉCHARGEMENT PDF :
@app.route('/download', methods=['POST'])
def download():
    if 'week' not in session:
        return redirect(url_for('index'))

    start = session['week'] * 7
    end = min(start + 7, session['jours'])
    plan_data = {f"Jour {i+1}": all_plans[i] for i in range(start, end)}

    html = render_template_string("""
    <html>
    <head>
    <meta charset="UTF-8">
    <style>
    body { font-family: Arial, sans-serif; font-size: 12px; }
    table { width: 100%; border-collapse: collapse; margin-top: 20px; }
    th, td { border: 1px solid black; padding: 5px; }
    th { background-color: #00cc66; color: black; }
    </style>
    </head>
    <body>
    <h1>Programme ELIO - Semaine {{ semaine }} sur {{ total_semaines }}</h1>
    <h2>Âge : {{ age }} ans | Taille : {{ taille }} cm | Poids : {{ poids }} kg | Objectif : {{ objectif }}</h2>
    <table>
      <thead>
        <tr>
          <th>Jour</th>
          <th>Petit-déjeuner</th>
          <th>Déjeuner</th>
          <th>Dîner</th>
          <th>Exercices</th>
        </tr>
      </thead>
      <tbody>
      {% for jour, plan in plan_data.items() %}
        <tr>
          <td>{{ jour }}</td>
          <td>{{ plan['repas']['petit_dejeuner']['nom'] }}</td>
          <td>{{ plan['repas']['dejeuner']['nom'] }}</td>
          <td>{{ plan['repas']['diner']['nom'] }}</td>
          <td>
            {{ plan['echauffement'] }}<br>
            {% for ex in plan['exercices'] %}
              {{ ex['nom'] }} ({{ ex['repetitions'] }})<br>
            {% endfor %}
          </td>
        </tr>
      {% endfor %}
      </tbody>
    </table>
    </body>
    </html>
    """, 
    semaine=session['week'] + 1,
    total_semaines=(session['jours'] - 1) // 7 + 1,
    age=session['age'],
    taille=session['taille'],
    poids=session['poids'],
    objectif=session['objectif'],
    plan_data=plan_data)

    pdf = BytesIO()
    pisa_status = pisa.CreatePDF(html, dest=pdf)
    if pisa_status.err:
        return "Erreur lors de la création du PDF"

    response = make_response(pdf.getvalue())
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'attachment; filename=Programme_Elio_Semaine.pdf'
    return response

if __name__ == '__main__':
    app.run(debug=True)
