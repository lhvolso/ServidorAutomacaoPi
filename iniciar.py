import RPi.GPIO as GPIO
from flask import Flask, request, json
#from flask import jsonify
from flask_cors import CORS, cross_origin

app = Flask(__name__)
cors = CORS(app)
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

@app.route("/")
def hello():
    return "<h1>Seu servidor foi iniciado corretamente</h1>"

@app.route("/controle", methods=["GET","POST"])
@cross_origin()
def controle():
    json = request.json
    pinoacende = int(json.get('pinoacende'))
    pinoretorno = int(json.get('pinoretorno'))
    status = int(json.get('status'))

    GPIO.setup(pinoacende, GPIO.OUT)
    GPIO.setup(pinoretorno, GPIO.IN)

    if status == 1:
        GPIO.output(pinoacende, GPIO.HIGH)
    if status == 0:
        GPIO.output(pinoacende, GPIO.LOW)

    return '{"sucesso":"true"}'

@app.route("/salvar", methods=["GET","POST"])
@cross_origin()
def salvar():
    # app.logger.debug();

    # Le os dados de configuracao CRON
    with open("cron.json","r") as d:
        dados = json.load(d);
    
    # Adiciona os novos dados no respectivo indice
    dados['controle']['0'] = {"ligar":"8:00","desligar":"10:00","pinoacende":"11"}
        
    # Grava nos dados de configuracao CRON
    with open("cron.json","w") as d:
        d.write(json.dumps(dados))
        
    return '{"sucesso":"true"}'


if __name__ == "__main__":
     app.run(host='0.0.0.0', port=80, debug=True)













