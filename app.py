from flask import Flask, render_template, request
import math, forms

app = Flask(__name__)

@app.route('/index')
def index():
    titulo = "Pagina de inicio"
    lista = ["Python", "Flask", "HTML", "CSS", "JavaScript"]
    return render_template('index.html', titulo=titulo, lista=lista)

@app.route('/calculos', methods=['GET', 'POST'])
def calculos():
    
    if request.method == 'POST':
        numer1 = request.form['numero1']
        numer2 = request.form['numero2']
        opcion = request.form['opcion']  
        if opcion == 'suma':
            calcu = int(numer1) + int(numer2)
        elif opcion == 'resta':
            calcu = int(numer1) - int(numer2)
        elif opcion == 'multiplicacion':
            calcu = int(numer1) * int(numer2)
        elif opcion == 'division':
            calcu = int(numer1) / int(numer2)
        return render_template('calculos.html', calcu=calcu, numer1=numer1, numer2=numer2)
    return render_template('calculos.html')

@app.route('/distancia', methods=['GET', 'POST'])
def distancia():

    if request.method == 'POST':
        num1 = float(request.form['numero1'])
        num2 = float(request.form['numero2'])
        num3 = float(request.form['numero3'])
        num4 = float(request.form['numero4'])
        distancia = math.sqrt(math.pow(num3 - num1, 2) + math.pow(num4 - num2, 2))
        return render_template('distancia.html', distancia=distancia, num1=num1, num2=num2, num3=num3, num4=num4)
    return render_template('distancia.html')

@app.route('/alumnos', methods=['GET','POST'])
def alumnos():
    mat=0
    nom=""
    ape=""
    email=""
    alumno_clas=forms.UserForm(request.form)
    if request.method == 'POST' and alumno_clas.validate():
        mat=alumno_clas.matricula.data
        nom=alumno_clas.nombre.data
        ape=alumno_clas.apellido.data
        email=alumno_clas.correo.data

    return render_template('alumnos.html', form=alumno_clas, mat=mat, nom=nom, ape=ape, email=email)

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