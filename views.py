from flask import Flask, render_template, request, redirect, session, flash, url_for
from models import Carro
from config import app, db
from dao import CarroDao, UsuarioDao


carro_dao = CarroDao(db)


@app.route('/')
@app.route('/index')
def index():
    return render_template('lista.html', titulo='Carros', carros=carro_dao.listar())


@app.route('/novo')
def novo():
    if 'usuário logado' not in session or session['usuário logado'] == None:
        return redirect(url_for('login', proxima=url_for('novo')))
    return render_template('novo.html', titulo='Novo carro')


@app.route('/criar', methods=['POST', ])
def criar():
    global carro_dao
    marca = request.form['marca']
    modelo = request.form['modelo']
    cor = request.form['cor']
    combustivel = request.form['combustivel']
    ano = request.form['ano']
    carro = Carro(id = None, marca= marca, modelo = modelo, cor = cor, combustivel = combustivel, ano = ano)
    car = carro_dao.salvar(carro)
    return redirect(url_for('index'))


@app.route("/login")
def login():
    proxima = request.args.get('proxima')
    return render_template('login.html', titulo='Login', proxima=proxima)


@app.route("/autenticar",  methods=['POST', ])
def autenticar():
    if "12345" == request.form['senha']:
        session['usuário logado'] = request.form['usuario']
        flash(request.form['usuario'] + 'logou com sucesso')
        proxima_pagina = request.form['proxima']
        return redirect((proxima_pagina))
    else:
        flash('Usuário ou senha incorreta, tente novamente')
        return redirect(url_for('login'))


@app.route('/logout')
def logout():
    session['usuário logado'] = None
    flash('Nenhum usuário logado')
    return redirect(url_for('index'))
