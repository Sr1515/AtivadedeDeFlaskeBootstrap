from flask import Flask, render_template, request, redirect

app = Flask(__name__)


class Carro:
    def __init__(self, id, marca, modelo, cor, combustivel, ano):
        self.id = id
        self.marca = marca
        self.modelo = modelo
        self.cor = cor
        self.combustivel = combustivel
        self.ano = ano


carro1 = Carro('001', 'Fiat', 'Uno', 'azul', 'etanol', '2021')
carro2 = Carro('002', 'Fiat', 'Touro', 'vermelho', 'gasolina', '2020')
lista = [carro1, carro2]


@app.route('/')
def index():
    return render_template('lista.html', titulo='Carros', carros=lista)


@app.route('/novo')
def novo():
    return render_template('novo.html', titulo='Novo carro')


@app.route('/criar', methods=['POST', ])
def criar():
    id = request.form['id']
    marca = request.form['marca']
    modelo = request.form['modelo']
    cor = request.form['cor']
    combustivel = request.form['combustivel']
    ano = request.form['ano']
    carro = Carro(id, marca, modelo, cor, combustivel, ano)
    lista.append(carro)
    return redirect('/')


app.run(debug=True)
