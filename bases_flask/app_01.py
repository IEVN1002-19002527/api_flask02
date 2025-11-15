from flask import Flask, render_template, request, make_response, jsonify, json
import math, forms, pforms

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
    tem=[]
    estudiantes=[]
    datos=[]

    alumno_clas=forms.UserForm(request.form)
    if request.method == 'POST' and alumno_clas.validate():
        if request.form.get("btnElimina")=='eliminar':
            response = make_response(render_template('Alumnos.html',))
            response.delete_cookie('usuario')

        mat=alumno_clas.matricula.data
        nom=alumno_clas.nombre.data
        ape=alumno_clas.apellido.data
        email=alumno_clas.correo.data

        datos={'matricula':mat,'nombre':nom.rstrip(),
               'apellido':ape.rstrip(),'email':email.rstrip()}  
        data_str = request.cookies.get("usuario")
        if not data_str:
             return "No hay cookie guardada", 404
        #estudiantes = json.loads(data_str)
        #estudiantes.append(datos)  
    response=make_response(render_template('Alumnos.html',
            form=alumno_clas, mat=mat, nom=nom, apell=ape, email=email))
    
    if request.method == 'GET':
        response.set_cookie('usuario', json.dumps(tem))

    return response

@app.route('/pizzeria', methods=['GET', 'POST'])
def pizzeria():
    from datetime import datetime
    
    nombre=""
    direccion=""
    telefono=""
    fecha=""
    tamano=""
    ingredientes=""
    npizzas=""
    pizzas_pedido = []  # Lista de pizzas en el pedido actual
    mensaje = ""  # Mensaje para mostrar al usuario
    total_pedido = 0
    ventas_acumuladas = []  # Lista de todas las ventas realizadas

    # Definición de precios
    precios_tamano = {'chica': 40, 'mediana': 80, 'grande': 120}
    precio_ingrediente = 10  # Precio por cada ingrediente adicional

    # Crear instancia del formulario
    piz_clas = pforms.UserForm(request.form)
    
    # Cargar pizzas del pedido actual desde cookie
    pedido_str = request.cookies.get("pedido_pizzas")
    if pedido_str:
        try:
            pizzas_pedido = json.loads(pedido_str)
            # Convertir valores numéricos a enteros para evitar errores de tipo
            for pizza in pizzas_pedido:
                if 'subtotal' in pizza:
                    try:
                        if isinstance(pizza['subtotal'], str):
                            pizza['subtotal'] = int(float(pizza['subtotal']))
                        else:
                            pizza['subtotal'] = int(pizza['subtotal'])
                    except (ValueError, TypeError):
                        pizza['subtotal'] = 0
                else:
                    pizza['subtotal'] = 0
                    
                if 'npizzas' in pizza:
                    try:
                        if isinstance(pizza['npizzas'], str):
                            pizza['npizzas'] = int(float(pizza['npizzas']))
                        else:
                            pizza['npizzas'] = int(pizza['npizzas'])
                    except (ValueError, TypeError):
                        pizza['npizzas'] = 0
                else:
                    pizza['npizzas'] = 0
        except Exception as e:
            pizzas_pedido = []
    
    # Cargar ventas acumuladas desde cookie
    ventas_str = request.cookies.get("cookie_ventas")
    if ventas_str:
        try:
            ventas_acumuladas = json.loads(ventas_str)
            # Convertir totales a enteros para consistencia de datos
            for venta in ventas_acumuladas:
                if 'total' in venta:
                    venta['total'] = int(venta['total'])
        except:
            ventas_acumuladas = []
    
    # Cargar datos del cliente desde cookie si existen (para mantener datos entre recargas)
    cliente_str = request.cookies.get("datos_cliente")
    if cliente_str and not nombre:
        try:
            cliente_data = json.loads(cliente_str)
            nombre = cliente_data.get('nombre', '')
            direccion = cliente_data.get('direccion', '')
            telefono = cliente_data.get('telefono', '')
            fecha = cliente_data.get('fecha', datetime.now().strftime("%d-%m-%Y"))
        except:
            pass
    
    # Establecer fecha actual si no existe
    if not fecha:
        fecha = datetime.now().strftime("%d-%m-%Y")

    if request.method == 'POST':
        # Procesar acción del botón "Agregar"
        if request.form.get("btnAgregar") == 'agregar':
            # Obtener datos del formulario
            nombre = request.form.get('nombre', '')
            direccion = request.form.get('direccion', '')
            telefono = request.form.get('telefono', '')
            fecha = datetime.now().strftime("%d-%m-%Y")  # Fecha automática
            
            tamano = request.form.get('tamano', '')
            ingredientes_list = request.form.getlist('ingredientes')  # Lista de ingredientes seleccionados
            npizzas = request.form.get('npizzas', '')
            
            # Validar que todos los campos requeridos estén completos
            if nombre and direccion and telefono and tamano and npizzas:
                # Calcular precio: base + ingredientes adicionales
                precio_base = precios_tamano.get(tamano, 0)
                precio_ingredientes = len(ingredientes_list) * precio_ingrediente
                precio_unitario = precio_base + precio_ingredientes
                subtotal = precio_unitario * int(npizzas)  # Total para esta pizza
                
                # Crear objeto pizza con todos los datos
                pizza_item = {
                    'tamano': tamano,
                    'ingredientes': ', '.join(ingredientes_list) if ingredientes_list else 'Ninguno',
                    'npizzas': int(npizzas),
                    'subtotal': int(subtotal)
                }
                
                # Agregar pizza al pedido actual
                pizzas_pedido.append(pizza_item)
                
                # Preparar datos del cliente para guardar en cookie
                datos_cliente = {
                    'nombre': nombre,
                    'direccion': direccion,
                    'telefono': telefono,
                    'fecha': fecha
                }
                
                mensaje = ""
            else:
                mensaje = "Por favor complete todos los campos requeridos"
        
        # Procesar acción del botón "Quitar"
        elif request.form.get("btnQuitar") == 'quitar':
            indice_str = request.form.get("indice_quitar")
            if indice_str:
                try:
                    indice = int(indice_str)
                    # Validar que el índice esté dentro del rango válido
                    if 0 <= indice < len(pizzas_pedido):
                        pizzas_pedido.pop(indice)  # Eliminar pizza del pedido
                        mensaje = ""
                except:
                    mensaje = "Error al eliminar la pizza"
        
        # Procesar acción del botón "Terminar"
        elif request.form.get("btnTerminar") == 'terminar':
            if pizzas_pedido:
                # Calcular el total del pedido sumando todos los subtotales
                total_pedido = 0
                for p in pizzas_pedido:
                    try:
                        subtotal = p.get('subtotal', 0)
                        if isinstance(subtotal, str):
                            subtotal = float(subtotal)
                        total_pedido += int(subtotal)
                    except (ValueError, TypeError):
                        continue
                
                # Obtener datos del cliente del formulario
                nombre = request.form.get('nombre', '')
                direccion = request.form.get('direccion', '')
                telefono = request.form.get('telefono', '')
                fecha = datetime.now().strftime("%d-%m-%Y")
                
                # Si no hay datos en el formulario, intentar obtenerlos de la cookie
                if not nombre:
                    cliente_str = request.cookies.get("datos_cliente")
                    if cliente_str:
                        try:
                            cliente_data = json.loads(cliente_str)
                            nombre = cliente_data.get('nombre', '')
                            direccion = cliente_data.get('direccion', '')
                            telefono = cliente_data.get('telefono', '')
                            fecha = cliente_data.get('fecha', datetime.now().strftime("%d-%m-%Y"))
                        except:
                            pass
                
                # Crear registro de venta y agregarlo a las ventas acumuladas
                venta = {
                    'nombre': nombre,
                    'direccion': direccion,
                    'telefono': telefono,
                    'fecha': fecha,
                    'total': total_pedido
                }
                ventas_acumuladas.append(venta)
                
                # Mostrar mensaje de confirmación con el total
                mensaje = f"Pedido terminado. Total a pagar: ${total_pedido}"
                
                # Limpiar el pedido actual después de finalizar
                pizzas_pedido = []
        
        # Botón Eliminar (limpiar todo)
        elif request.form.get("btnElimina") == 'eliminar':
            pizzas_pedido = []
            mensaje = "Pedido eliminado"

    # Preparar datos para mostrar en el template
    # Calcular el total del pedido actual (suma de todos los subtotales)
    total_actual = 0
    for p in pizzas_pedido:
        try:
            subtotal = p.get('subtotal', 0)
            if isinstance(subtotal, str):
                subtotal = float(subtotal)
            total_actual += int(subtotal)
        except (ValueError, TypeError):
            continue
    
    # Calcular ventas totales del día actual
    fecha_hoy = datetime.now().strftime("%d-%m-%Y")
    ventas_hoy = [v for v in ventas_acumuladas if v.get('fecha') == fecha_hoy]
    total_dia = sum(int(v.get('total', 0)) for v in ventas_hoy)
    
    # Agrupar ventas por cliente para mostrar resumen
    ventas_por_cliente = {}
    for venta in ventas_acumuladas:
        nombre_cliente = venta.get('nombre', 'Sin nombre')
        if nombre_cliente not in ventas_por_cliente:
            ventas_por_cliente[nombre_cliente] = 0
        ventas_por_cliente[nombre_cliente] += int(venta.get('total', 0))
    
    # Renderizar template con todos los datos necesarios
    response = make_response(render_template('pizzeria.html',
        form=piz_clas,
        nombre=nombre,
        direccion=direccion,
        telefono=telefono,
        fecha=fecha,
        tamano=tamano,
        ingredientes=ingredientes,
        npizzas=npizzas,
        pizzas_pedido=pizzas_pedido,
        mensaje=mensaje,
        total_pedido=total_pedido,
        total_actual=total_actual,
        ventas_por_cliente=ventas_por_cliente,
        total_dia=total_dia))
    
    # Guardar datos en cookies para persistencia entre recargas
    # Convertir valores numéricos a enteros antes de serializar a JSON
    pizzas_para_guardar = []
    for pizza in pizzas_pedido:
        pizza_guardar = {
            'tamano': pizza.get('tamano', ''),
            'ingredientes': pizza.get('ingredientes', ''),
            'npizzas': int(pizza.get('npizzas', 0)),
            'subtotal': int(pizza.get('subtotal', 0))
        }
        pizzas_para_guardar.append(pizza_guardar)
    
    # Guardar pedido actual y ventas acumuladas en cookies
    response.set_cookie('pedido_pizzas', json.dumps(pizzas_para_guardar))
    response.set_cookie('cookie_ventas', json.dumps(ventas_acumuladas))
    
    # Guardar datos del cliente en cookie si existen
    if nombre:
        datos_cliente = {
            'nombre': nombre,
            'direccion': direccion,
            'telefono': telefono,
            'fecha': fecha
        }
        response.set_cookie('datos_cliente', json.dumps(datos_cliente))

    return response

@app.route("/get_cookie")
def get_cookie():
     
    data_str = request.cookies.get("tem")
    if not data_str:
        return "No hay cookie guardada", 404
 
    pizzas = json.loads(data_str)
 
    return jsonify(pizzas)

# @app.route('/user/<string:user>')
# def user(user):
#     return f"Hello, {user}!"

# @app.route('/numero/<int:num>')
# def int(num):
#     return f"Hello, {num}!"

# @app.route('/suma/<int:num1>/<int:num2>')
# def suma(num1, num2):
#     return f"La suma es: {num1 + num2}"

# @app.route("/user/<int:id>/<string:username>")
# def username(id, username):
#     return "ID: {} nombre: {}".format(id, username)

# @app.route("/suma/<float:n1>/<float:n2>")
# def func1(n1, n2):
#     return "La suma es: {}".format(n1 + n2)

# @app.route("/default/")
# @app.route("/default/<string:dft>")
# def func2(dft="sss"):
#     return "El valor de dft es: " + dft

# @app.route("/prueba")
# def func3():
#     return '''
#     <html>
#     <head>
#     <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-EVSTQN3/azprG1Anm3QDgpJLIm9Nao0Yz1ztcQTwFspd3yD65VohhpuuCOmLASjC" crossorigin="anonymous">
#         <title>Pagina dePrueba</title>
#     </head>
#     <body>
#         <h1>Hola esta es una pagina de Prueba</h1>
#         <p>Esta pagina es para probar el retorno de HTML en Flask</p>
#     </body>
#     </html>
#     '''

if __name__ == '__main__':
    app.run(debug=True)