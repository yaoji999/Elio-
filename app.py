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
    from flask import send_file
from jinja2 import Template
from weasyprint import HTML

@app.route('/download-pdf', methods=['POST'])
def download_pdf():
    from io import BytesIO
    plan_data = request.form.get('plans_json')
    import json
    plans = json.loads(plan_data)

    # Exemple : on ne prend que le premier jour pour démo, tu peux élargir à plusieurs
    plan = plans[0]

    template_graphique = Template("""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <style>
            body { font-family: 'Helvetica Neue', sans-serif; background: #f7f7f7; color: #222; padding: 30px; }
            .container { background: white; border-radius: 12px; padding: 30px; box-shadow: 0 0 10px rgba(0,0,0,0.1); }
            h1 { text-align: center; font-size: 26px; margin-bottom: 20px; }
            h2 { border-bottom: 1px solid #ddd; padding-bottom: 5px; margin-top: 20px; }
            ul { padding-left: 20px; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Programme ELIO – {{ plan["Jour"] }}</h1>
            <h2>Nutrition</h2>
            <p><strong>Petit déjeuner :</strong> {{ plan["Petit déjeuner"] }}</p>
            <p><strong>Déjeuner :</strong> {{ plan["Déjeuner"] }}</p>
            <p><strong>Dîner :</strong> {{ plan["Dîner"] }}</p>

            <h2>Exercices</h2>
            <ul>
                <li>{{ plan["Exercice 1"] }}</li>
                <li>{{ plan["Exercice 2"] }}</li>
                <li>{{ plan["Exercice 3"] }}</li>
                <li>{{ plan["Exercice 4"] }}</li>
                <li>{{ plan["Exercice 5"] }}</li>
            </ul>
        </div>
    </body>
    </html>
    """)

    rendered_html = template_graphique.render(plan=plan)
    pdf_io = BytesIO()
    HTML(string=rendered_html).write_pdf(pdf_io)
    pdf_io.seek(0)

    return send_file(pdf_io, mimetype='application/pdf', download_name='programme_elio.pdf')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
