from flask import Flask, request, render_template, redirect, url_for, session

app = Flask(__name__)

# Necesario para poder usar sesiones
app.secret_key = 'unaclavesecreta'

# Función para generar el ID de los productos
def generar_id():
    # Corregido: Cambié 'contacto' por 'productos' para acceder correctamente a la lista de productos.
    if 'productos' in session and len(session['productos']) > 0:
        return max(item['id'] for item in session['productos']) + 1
    else:
        return 1

@app.route("/")
def index():
    # Corregido: Verificación correcta de si 'contactos' no está en la sesión
    if 'productos' not in session:
        session['productos'] = []  # Inicializa la lista de contactos en la sesión si no existe
    
    # Obtiene los contactos de la sesión
    productos = session.get('productos', [])
    return render_template('index.html', productos=productos)

# Ruta para agregar un nuevo contacto
@app.route("/nuevo", methods=['GET', 'POST'])
def nuevo():
    if request.method == 'POST':
        # Se capturan los datos del formulario
        nombre = request.form['nombre']
        cantidad = int(request.form['cantidad'])
        precio = float(request.form['precio'])
        fecha_ven = request.form['fecha_ven']
        categoria = request.form.getlist('categoria')
        
        # Se crea un diccionario para el nuevo contacto
        nuevo_producto = {
            'id': generar_id(),
            'nombre': nombre,
            'cantidad': cantidad,
            'precio': precio,
            'fecha_ven': fecha_ven,
            'categoria': categoria
        }
        
        # Verifica si 'contactos' no está en la sesión, lo inicializa si es necesario
        if 'productos' not in session:
            session['productos'] = []
        
        # Se agrega el nuevo contacto a la lista de la sesión
        session['productos'].append(nuevo_producto)
        session.modified = True  # Marca la sesión como modificada
        return redirect(url_for('index'))
    
    return render_template('nuevo.html')

# Ruta para editar un contacto existente
@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    # Obtiene la lista de contactos de la sesión
    lista_productos = session.get('productos', [])
    # Busca el contacto a editar según su ID
    producto = next((c for c in lista_productos if c['id'] == id), None)  # Corregido: Eliminé el espacio extra
    
    # Si no se encuentra el contacto, redirige al index
    if not producto:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        # Actualiza los valores del contacto
        producto['nombre'] = request.form['nombre']
        producto['cantidad'] = request.form['cantidad']
        producto['precio'] = request.form['precio']
        producto['fecha_ven'] = request.form['fecha_ven']
        producto['categoria'] = request.form.getlist('categoria')
        session.modified = True  # Marca la sesión como modificada
        return redirect(url_for('index'))
    
    return render_template('editar.html', producto=producto)

# Ruta para eliminar un contacto
@app.route("/eliminar/<int:id>", methods=["POST"])  # Corregido: Cambié "/elminar" a "/eliminar"
def eliminar(id):
    # Obtiene la lista de contactos de la sesión
    lista_productos = session.get('productos', [])
    # Busca el contacto a eliminar según su ID
    producto = next((c for c in lista_productos if c['id'] == id), None)  # Corregido: Eliminé el espacio extra
    
    # Si se encuentra el contacto, se elimina de la lista
    if producto:
        session['productos'].remove(producto)
        session.modified = True  # Marca la sesión como modificada
    
    return redirect(url_for('index'))

# Corre la aplicación en modo debug
if __name__ == "__main__":
    app.run(debug=True)
