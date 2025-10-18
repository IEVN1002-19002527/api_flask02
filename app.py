from flask import Flask, render_template

app = Flask(__name__)

@app.route('/index')
def index():
    titulo = "Pagina de inicio"
    lista = ["Python", "Flask", "HTML", "CSS", "JavaScript"]
    return render_template('index.html', titulo=titulo, lista=lista)

@app.route('/calculos')
def calculos():
    return render_template('calculos.html')

@app.route('/distancia')
def distancia():
    return render_template('distancia.html')

@app.route('/user/<string:user>')
def user(user):
    return f"Hello, {user}!"

@app.route('/numero/<int:num>')
def int(num):
    return f"Hello, {num}!"

@app.route('/suma/<int:num1>/<int:num2>')
def suma(num1, num2):
    return f"La suma es: {num1 + num2}"

@app.route("/user/<int:id>/<string:username>")
def username(id, username):
    return "ID: {} nombre: {}".format(id, username)

@app.route("/suma/<float:n1>/<float:n2>")
def func1(n1, n2):
    return "La suma es: {}".format(n1 + n2)

@app.route("/default/")
@app.route("/default/<string:dft>")
def func2(dft="sss"):
    return "El valor de dft es: " + dft

@app.route("/prueba")
def func3():
    return '''
    <html>
    <head>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-EVSTQN3/azprG1Anm3QDgpJLIm9Nao0Yz1ztcQTwFspd3yD65VohhpuuCOmLASjC" crossorigin="anonymous">
        <title>Pagina dePrueba</title>
    </head>
    <body>
        <h1>Hola esta es una pagina de Prueba</h1>
        <p>Esta pagina es para probar el retorno de HTML en Flask</p>
    </body>
    </html>
    '''

if __name__ == '__main__':
    app.run(debug=True)