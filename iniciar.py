#!/usr/bin/python
import time, RPi.GPIO as GPIO
from flask import Flask, request, json
#from flask import jsonify
from flask_cors import CORS, cross_origin

app = Flask(__name__)
cors = CORS(app)
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

@app.route("/", methods=["GET","POST"])
@cross_origin()
def padrao():
    return '<h1>Seu servidor foi iniciado corretamente</h1>'

@app.route("/lerpinos", methods=["GET","POST"])
@cross_origin()
def lerpinos():
    json = request.json
    pinoretorno = int(json.get('pinoretorno'))
    GPIO.setup(pinoretorno, GPIO.IN, pull_up_down = GPIO.PUD_UP)
    ligado = GPIO.input(pinoretorno)
    return '{"ligado":"'+str(ligado)+'"}'

@app.route("/controle", methods=["GET","POST"])
@cross_origin()
def controle():
    json = request.json
    pinoacende = int(json.get('pinoacende'))
    pinoretorno = int(json.get('pinoretorno'))
    status = int(json.get('status'))
    GPIO.setup(pinoacende, GPIO.OUT)
    GPIO.setup(pinoretorno, GPIO.IN, pull_up_down = GPIO.PUD_UP)
    
    statuspinoacende = GPIO.input(pinoacende)
    statuspinoretorno = GPIO.input(pinoretorno)
    
    #app.logger.debug('Pino acende: ' + str(statuspinoacende))
    #app.logger.debug('Pino retorno: ' + str(statuspinoretorno))
    
    sucesso = 1

    GPIO.output(pinoacende, not statuspinoacende)
    while GPIO.input(pinoretorno) == (not statuspinoretorno):
        time.sleep(0.25)
        #app.logger.debug('while')
        if time.time() > timeout:
            sucesso = 0
            break

    time.sleep(0.25)
    statuspinoretorno = GPIO.input(pinoretorno);

    if sucesso:
        return '{"sucesso":"true", "ligado":'+str(statuspinoretorno)+'}'
    else:
        return '{"sucesso":"false"}'

@app.route("/salvar", methods=["GET","POST"])
@cross_origin()
def salvar():
    # app.logger.debug()
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













