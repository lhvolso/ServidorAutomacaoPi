#!/usr/bin/python
import time, logging, RPi.GPIO as GPIO
from flask import Flask, request, json
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
    # app.logger.debug(dadosJson)
    dadosJson = request.json
    pinoacende = dadosJson.get('pinoacende')
    pinoretorno = dadosJson.get('pinoretorno')
    indice = dadosJson.get('indice')
    horaacende = dadosJson.get('horaacende')
    horaapaga = dadosJson.get('horaapaga')
    with open("/home/pi/ServidorAutomacaoPi/cron.json","r") as d:
        try:
            dados = json.load(d)
        except:
            dados = {}

    dados.update({""+indice+"":{"ligar":""+horaacende+"","desligar":""+horaapaga+"","pinoacende":""+pinoacende+"","pinoretorno":""+pinoretorno+""}})
    
    with open("/home/pi/ServidorAutomacaoPi/cron.json","w") as d:
        d.write(json.dumps(dados))

    return '{"sucesso":"true"}'

@app.route("/deletar", methods=["GET","POST"])
@cross_origin()
def deletar():
    dadosJson = request.json
    indice = dadosJson.get('indice')
    with open("/home/pi/ServidorAutomacaoPi/cron.json","r") as d:
        dados = json.load(d)

    del dados[indice]

    with open("/home/pi/ServidorAutomacaoPi/cron.json","w") as d:
        d.write(json.dumps(dados))

    return '{"sucesso":"true"}'

if __name__ == "__main__":
    # logging.basicConfig(filename='error.log',level=logging.DEBUG)
    app.run(host='0.0.0.0', port=80, debug=True)