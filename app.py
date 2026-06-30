from flask import Flask, request, render_template, redirect, url_for, flash, jsonify, make_response
from database import db
from math import ceil

app = Flask(__name__)

app.secret_key = "s3cr3t_k3y"

@app.route("/")
def portada():
    return render_template("portada.html")

@app.route("/carreras", methods=["GET", "POST"])
def carreras():
    if request.method == "GET":
        return render_template("carreras.html")
    else:
        data = request.get_json()
        items_per_page = 20
        pagina = int(data.get("page")) 
        query = data.get("query", "")
        jornada = data.get("jornada", "")
        modalidad = data.get("modalidad", "")
        nivel = data.get("nivel", "")
        total_paginas = ceil(int(db.total_carreras(query, jornada, modalidad, nivel)[0])/items_per_page)
        carreras = db.free_search_carrera(query, jornada, modalidad, pagina, items_per_page, nivel)
        body = {"total_paginas": total_paginas,
                "carreras": [dict(row._mapping) for row in carreras]}
        return jsonify(body)

@app.route("/distr_genero", methods=["GET", "POST"])
def distr_genero():
    if request.method == "GET":
        return render_template("distr_genero.html")
    else:
        data = request.get_json()
        institucion = data.get("institucion")
        data = db.get_distr_genero(institucion)
        total = 0
        for r in data:
            total += r.total
        print([dict(row._mapping) for row in data])
        body = {"result": [dict(row._mapping) for row in data],
                "abs_total": total}
        return jsonify(body)

@app.route("/over_thirty", methods=["GET", "POST"])
def over_thirty():
    if request.method == "GET":
        return render_template("over_thirty.html")
    else:
        data = request.get_json()
        items_per_page = 10
        pagina = int(data.get("page")) 
        minimum = data.get("min", "")
        total_paginas = ceil(int(db.total_total_over_30(minimum)[0])/items_per_page)
        data = db.total_over_30(minimum, pagina, items_per_page)
        body = {"total_paginas": total_paginas,
                "data": [dict(row._mapping) for row in data]}
        return jsonify(body)
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
