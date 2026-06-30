from flask import Flask, session, request, render_template, redirect, url_for, flash, jsonify, make_response
from utils.validations import *
from database import db
from math import ceil
import os

app = Flask(__name__)

app.secret_key = "s3cr3t_k3y"

@app.route("/", methods=["GET", "POST"])
def portada():
    if request.method == "GET":
        return render_template("portada.html")
    else:
        data = request.get_json()
        items_per_page = 20
        pagina = int(data.get("page")) 
        print(pagina)
        query = data.get("query", "")
        jornada = data.get("jornada", "")
        modalidad = data.get("modalidad", "")
        nivel = data.get("nivel", "")
        total_paginas = ceil(int(db.total_carreras(query, jornada, modalidad, nivel)[0])/items_per_page)
        carreras = db.free_search_carrera(query, jornada, modalidad, pagina, items_per_page, nivel)
        body = {"total_paginas": total_paginas,
                "carreras": [dict(row._mapping) for row in carreras]}
        return jsonify(body)



    
if __name__ == "__main__":
    app.run(debug=True)