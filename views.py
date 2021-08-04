from flask import Flask, render_template, request, redirect, session, flash, url_for
from models import Carro, Usuario
from config import app, db
from dao import CarroDao, UsuarioDao

carro_dao = CarroDao(db)
usuario_dao = UsuarioDao(db)


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        pesquisa = request.form['pesquisa']
    else:
        pesquisa = None
    return render_template('lista.html', titulo='Carros', carros=carro_dao.listar(pesquisa), tamanho=len(carro_dao.listar(pesquisa)) == 0)


@app.route('/novo')
def novo():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('novo')))
    return render_template('novo.html', titulo='Novo Carro')


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

@app.route('/editar/<int:id>')
def editar(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('editar', id=id)))
    carro = carro_dao.busca_por_id(id)
    return render_template('editar.html', titulo='Editando Carro', carro = carro)

@app.route('/atualizar', methods=['POST', ])
def atualizar():
    marca = request.form['marca']
    modelo = request.form['modelo']
    cor = request.form['cor']
    combustivel = request.form['combustivel']
    ano = request.form['ano']
    id = request.form['id']
    carro = Carro(marca= marca, modelo = modelo, cor = cor, combustivel = combustivel, ano = ano, id = id)
    car = carro_dao.salvar(carro)
    return redirect(url_for('index'))

@app.route('/deletar/<int:id>')
def deletar(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('deletar', id=id)))
    carro_dao.deletar(id)
    flash('o livro foi removido com sucesso')
    return redirect(url_for('index'))


@app.route("/login")
def login():
    proxima = request.args.get('proxima')
    return render_template('login.html', titulo='Login', proxima=proxima)

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    global usuario_dao
    if request.method == 'POST':
        username = request.form['username']
        name = request.form['name']
        password = request.form['password']
        
        usuario = Usuario(id = username, nome=name, senha=password)
        user = usuario_dao.salvar(usuario)
        return redirect(url_for('login'))
    return render_template('cadastrar.html', titulo='Cadastrar')


@app.route("/autenticar",  methods=['POST', ])
def autenticar():
    usuario = usuario_dao.autenticar(request.form['usuario'], request.form['senha'])
    if usuario:
            session['usuario_logado'] = usuario.id
            flash(usuario.nome + 'logou com sucesso')
            proxima_pagina = request.form['proxima']
            return redirect((proxima_pagina))
        
    else:
        flash('Usuário ou senha incorreta, tente novamente')
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session['usuario_logado'] = None
    flash('Nenhum usuário logado')
    return redirect(url_for('index'))

