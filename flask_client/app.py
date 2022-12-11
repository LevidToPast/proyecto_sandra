from flask import Flask, render_template, request
import openai

openai.api_key = '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'

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/registrar_calificaciones")
def registrar_calificaciones():
    return render_template("registrar_calificaciones.html")

@app.route("/consultar_pagos")
def consultar_pagos():
    return render_template("consultar_pagos.html")

@app.route("/registrar_pago")
def registrar_pago():
    return render_template('registrar_pagos.html')

@app.route("/servicio_gratuito")
def servicio_gratuito():
    return render_template("servicio_gratuito.html")

@app.route("/generar_imagen", methods=["POST"])
def generar_imagen():
    if request.method == 'POST':
        request_json = request.get_json()
        print(request_json)
        response = openai.Image.create(
            prompt=request_json['text'],
            n=1,
            size="1024x1024"
        )
        image_url = response['data'][0]['url']
        return {"url": image_url}
    

if __name__ == '__main__':
    app.run("0.0.0.0", 8001, True)