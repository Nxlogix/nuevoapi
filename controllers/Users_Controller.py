from models.User import Usuario
from flask import jsonify
from config import db
from flask_jwt_extended import create_access_token
from werkzeug.security import generate_password_hash

def create_usuario(nombre, email, password):
    try:
        nuevo_usuario = Usuario(nombre, email, password)
        db.session.add(nuevo_usuario)
        db.session.commit()
        return jsonify(nuevo_usuario.to_dict()), 201
    except Exception as e:
        print(f"ERROR {e}")
        return jsonify({'msg': 'Error al crear el nuevo usuario'}), 500

def login_usuario(email, password):
    try:
        usuario = Usuario.query.filter_by(email=email).first()
        if usuario and usuario.check_password(password):
            access_token = create_access_token(identity=usuario.id)
            return jsonify({
                'access_token': access_token,
                'usuario': usuario.to_dict()
            })
        return jsonify({"msg": "Datos incorrectos"}), 401
    except Exception as e:
        print(f"ERROR {e}")
        return jsonify({'msg': 'Error en el inicio de sesion'}), 500

def get_all_usuarios():
    try:
        usuarios = [usuario.to_dict() for usuario in Usuario.query.all()]
        return jsonify(usuarios)
    except Exception as error:
        print(f"ERROR {error}")
        return jsonify({'msg': f'Error al obtener los usuarios: {error}'}), 500

def get_usuario_by_id(id):
    try:
        usuario = Usuario.query.get(id)
        if not usuario:
            return jsonify({'msg': 'Usuario no encontrado'}), 404
        return jsonify(usuario.to_dict())
    except Exception as e:
        print(f"ERROR {e}")
        return jsonify({'msg': 'Error al obtener el usuario'}), 500

def update_usuario(id, data):
    try:
        usuario = Usuario.query.get(id)
        if not usuario:
            return jsonify({'msg': 'Usuario no encontrado'}), 404

        usuario.nombre = data.get('nombre', usuario.nombre)
        usuario.email = data.get('email', usuario.email)
        if 'password' in data:
            usuario.password = generate_password_hash(data['password'])

        db.session.commit()
        return jsonify({'msg': 'Usuario actualizado', 'usuario': usuario.to_dict()})
    except Exception as e:
        print(f"ERROR {e}")
        return jsonify({'msg': 'Error al actualizar el usuario'}), 500

def delete_usuario(id):
    try:
        usuario = Usuario.query.get(id)
        if not usuario:
            return jsonify({'msg': 'Usuario no encontrado'}), 404
        db.session.delete(usuario)
        db.session.commit()
        return jsonify({'msg': 'Usuario eliminado'})
    except Exception as e:
        print(f"ERROR {e}")
        return jsonify({'msg': 'Error al eliminar el usuario'}), 500
