from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

# Configuración de la aplicación Flask
app = Flask(__name__)

# Configurar la conexión a la base de datos MySQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@23.23.45.16/pruebas'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializar SQLAlchemy
db = SQLAlchemy(app)

# Definir el modelo de la tabla usuario
class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    pass_ = db.Column(db.String(100), nullable=False)  # Cambié el nombre de 'pass' a 'pass_' para evitar conflicto con palabra reservada

    def __repr__(self):
        return f'<Usuario {self.nombre}>'

# Crear las tablas en la base de datos
with app.app_context():
    db.create_all()

# Endpoint para obtener todos los usuarios
@app.route('/usuarios', methods=['GET'])
def get_usuarios():
    usuarios = Usuario.query.all()
    return jsonify([{'id': u.id, 'nombre': u.nombre} for u in usuarios])

# Endpoint para obtener un usuario por su ID
@app.route('/usuarios/<int:id>', methods=['GET'])
def get_usuario(id):
    usuario = Usuario.query.get(id)
    if usuario is None:
        return jsonify({'message': 'Usuario no encontrado'}), 404
    return jsonify({'id': usuario.id, 'nombre': usuario.nombre})

# Endpoint para crear un nuevo usuario
@app.route('/usuarios', methods=['POST'])
def create_usuario():
    data = request.get_json()
    nombre = data.get('nombre')
    pass_ = data.get('pass')

    if not nombre or not pass_:
        return jsonify({'message': 'Nombre y contraseña son obligatorios'}), 400

    nuevo_usuario = Usuario(nombre=nombre, pass_=pass_)
    db.session.add(nuevo_usuario)
    db.session.commit()

    return jsonify({'message': 'Usuario creado', 'id': nuevo_usuario.id}), 201

# Endpoint para actualizar un usuario
@app.route('/usuarios/<int:id>', methods=['PUT'])
def update_usuario(id):
    data = request.get_json()
    usuario = Usuario.query.get(id)
    
    if usuario is None:
        return jsonify({'message': 'Usuario no encontrado'}), 404

    usuario.nombre = data.get('nombre', usuario.nombre)
    usuario.pass_ = data.get('pass', usuario.pass_)

    db.session.commit()

    return jsonify({'message': 'Usuario actualizado'})

# Endpoint para eliminar un usuario
@app.route('/usuarios/<int:id>', methods=['DELETE'])
def delete_usuario(id):
    usuario = Usuario.query.get(id)

    if usuario is None:
        return jsonify({'message': 'Usuario no encontrado'}), 404

    db.session.delete(usuario)
    db.session.commit()

    return jsonify({'message': 'Usuario eliminado'})

# Iniciar la aplicación Flask
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
