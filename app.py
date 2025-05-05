from flask import Flask, render_template, request, send_file
import json
from io import BytesIO
from xhtml2pdf import pisa

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('elio_formulaire.html')

@app.route('/results', methods=['POST'])
def results():
    try:
        age = request.form['age']
        taille = request.form['taille']
        poids = request.form['poids']
        objectif = request.form['objectif']
        niveau = request.form['niveau']
        jours = int(request.form['jours'])
        regime = request.form['regime']

        with open('ELIO_Calories_90_Jours.json', 'r', encoding=' as f:
            data = json.load(f)

        plans = data[:jours]

        return render_template('results.html', age=age, taille=taille, poids=poids,
                               objectif=objectif, niveau=niveau, jours=jours,
                               regime=regime, plans=plans)
    except Exception as e:
        return f"Erreur dans le traitement des données : {str(e)}", 500

@app.route('/download-pdf', methods=['POST'])
def download_pdf():
    try:
        plan_data = request.form.get('plans_json')
        plans = json.loads(plan_data)
        plan = plans[0]

        html = f"""
        <html>
        <head>
            <style>
                body {{
                    font-family: Helvetica, sans-serif;
                    padding: 30px;
                    color: #222;
                }}
                h1 {{ text-align: center; }}
                h2 {{ margin-top: 30px; border-bottom: 1px solid #ccc; }}
                ul {{ margin-top: 10px; }}
            </style>
        </head>
        <body>
            <h1>Programme ELIO – {plan["Jour"]}</h1>

            <h2>Nutrition</h2>
            <p><strong>Petit déjeuner :</strong> {plan["Petit déjeuner"]}</p>
            <p><strong>Déjeuner :</strong> {plan["Déjeuner"]}</p>
            <p><strong>Dîner :</strong> {plan["Dîner"]}</p>

            <h2>Exercices</h2>
            <ul>
                <li>{plan["Exercice 1"]}</li>
                <li>{plan["Exercice 2"]}</li>
                <li>{plan["Exercice 3"]}</li>
                <li>{plan["Exercice 4"]}</li>
                <li>{plan["Exercice 5"]}</li>
            </ul>
        </body>
        </html>
        """

        result = BytesIO()
        pisa_status = pisa.CreatePDF(src=html, dest=result)

        if pisa_status.err:
            return "Erreur lors de la génération du PDF", 500

        result.seek(0)
        return send_file(result, mimetype='application/pdf', as_attachment=True, download_name='programme_elio.pdf')
    except Exception as e:
        return f"Erreur PDF : {str(e)}", 500

if __name__ == '__main__':
    app.run(debug=True)
