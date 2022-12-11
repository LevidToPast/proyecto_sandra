import os
import json
import random
from typing import List
from flask import Flask, request
from flask_restful import Resource, Api
from flask_cors import CORS, cross_origin
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session, DeclarativeMeta
from dotenv import load_dotenv

from structs import Alumnos, EstadoCuenta, Instituciones, TipoPagos, Calificaciones, Asignaturas
from models import Alumno, Pagos, Institucion, TipoPago, Asignatura, Calificacion

from sqlalchemy.ext.declarative import DeclarativeMeta

class AlchemyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj.__class__, DeclarativeMeta):
            # an SQLAlchemy class
            fields = {}
            for field in [x for x in dir(obj) if not x.startswith('_') and x != 'metadata']:
                data = obj.__getattribute__(field)
                try:
                    json.dumps(data) # this will fail on non-encodable values, like other classes
                    fields[field] = data
                except TypeError:
                    fields[field] = None
            # a json-encodable dict
            return fields

        return json.JSONEncoder.default(self, obj)
    
load_dotenv()

engine = create_engine(os.getenv('DATABASE_URL') , connect_args={'check_same_thread': False})

session: Session = sessionmaker(bind=engine)()

app = Flask(__name__)
api = Api(app)
cors = CORS(app)

class RutaEstadosCuenta(Resource):
    @cross_origin()
    def get(self, numero_matricula: str):
        alumno: Alumnos = session.query(Alumno).filter_by(
            numero_matricula=numero_matricula).first()
        
        if not alumno:
            return dict(
                estado=False, detail='No se encontró el alumno.')

        estados_cuenta: List[EstadoCuenta] = session.query(
            Pagos).filter_by(alumno_id=alumno.id).all()

        response = []
        for estado_cuenta in estados_cuenta:
            response.append(
                {
                    'id': estado_cuenta.id,
                    'alumno': estado_cuenta.alumno.nombres + ' ' + estado_cuenta.alumno.apellidos,
                    'pago': estado_cuenta.tipo_pago.tipo_pago,
                    'institucion': estado_cuenta.institucion.nombre,
                    'asignatura': estado_cuenta.asignatura.nombre
                }
            )

        return {'estado': True, 'estados_cuenta': response}
    
    @cross_origin()
    def post(self):
        pago: EstadoCuenta = request.get_json()
        print(pago)
        
        try:
            alumno: Alumno = session.query(Alumno).filter_by(
                numero_matricula=pago['numero_matricula']).first()
            
            if not alumno:
                return dict(estado=False, detail='Alumno solicidado no encontrado.')

            estado_cuenta = session.query(Pagos).filter_by(alumno_id=alumno.id, asignatura_id=pago.asignatura_id)
            
            if estado_cuenta:
                return dict(estado=400, detail='Pago solicitado ya ha sido registradp con anterioridad.')

            nuevo_pago = Pagos(
                alumno_id=alumno.id,
                tipo_pago_id=pago['tipo_pago_id'],
                institucion_id=pago['institucion_id'],
                asignatura_id=pago['asignatura_id']
            )
            session.add(nuevo_pago)
            session.commit()
            return {'estado': True, "mensaje": 'Pago registrado con éxito'}
        except Exception as e:
            print(e)
            session.rollback()
            return dict(
                estado=False, detail='Hubo un error al insertar el pago.')


class RutaInstituciones(Resource):
    @cross_origin()
    def get(self):
        try:
            institucion = session.query(Institucion).all()
            institucion = json.dumps(institucion, cls=AlchemyEncoder)
            return {'estado': True, 'mensaje': json.loads(institucion)}
        except Exception as e:
            print(e)
            return dict(
                estado=False, detail="Hubo un error al solicitar la lista de instituciones."), 400

    @cross_origin()
    def post(self):
        institucion: Instituciones = request.get_json()
        
        institucion_aux = session.query(Institucion).filter_by(
            nombre=institucion['nombre']).first()

        if institucion_aux:
            return dict(
                estado=False, detail='Institucion solicitada ya se encuentra en existencia'), 400

        try:
            nueva_institucion = Institucion(
                nombre=institucion['nombre']
            )
            session.add(nueva_institucion)
            session.commit()
            return {'estado': True, 'mensaje': 'La institución se ha agregado con exito.'}
        except Exception as e:
            session.rollback()
            print(e)
            return dict(
                estado=False, detail='Hubo un error al insertar la institución'), 400


class RutaAlumnos(Resource):
    @cross_origin()
    def get(self):
        try:
            alumnos = session.query(Alumno).all()
            response = json.dumps(alumnos, cls=AlchemyEncoder)
            return {'estado': True, 'mensaje': json.loads(response)}
        except Exception as e:
            print(e)
            return dict(
                estado=False, detail="Hubo un error al solicitar la lista de alumnos."), 400
            
    @cross_origin()
    def post(self):
        alumno: Alumnos = request.get_json()
        
        try:
            # genera una cadena random de 8 numeros
            numero_cuenta = str(random.randint(10000000, 99999999))
            nuevo_alumno = Alumno(
                numero_matricula=numero_cuenta,
                nombres=alumno['nombres'],
                apellidos=alumno['apellidos'],
                edad=alumno['edad'],
                email=alumno['email']
            )
            session.add(nuevo_alumno)
            session.commit()
            return {'estado': True, 'mensaje': 'El alumno se ha agregado con exito.'}
        except Exception as e:
            session.rollback()
            print(e)
            return dict(
                estado=False, detail='Hubo un error al insertar el alumno'), 400


class RutaTipoPagos(Resource):
    @cross_origin()
    def get(self):
        try:
            tipos_pagos = session.query(TipoPago).all()
            tipos_pagos = json.dumps(tipos_pagos, cls=AlchemyEncoder)
            return {'estado': True, 'mensaje': json.loads(tipos_pagos)}
        except Exception as e:
            print(e)
            return dict(
                estado=False, detail="Hubo un error al solicitar la lista de tipo de pagos."), 400
    
    @cross_origin()
    def post(self):
        tipo_pago: TipoPagos = request.get_json()
        try:
            nuevo_tipo_pago = TipoPago(
                tipo_pago=tipo_pago['tipo_pago']
            )
            session.add(nuevo_tipo_pago)
            session.commit()
            return {'estado': True, 'mensaje': 'El tipo de pago se ha agregado con exito.'}
        except Exception as e:
            print(e)
            session.rollback()
            return dict(
                estado=False, detail='Hubo un error al insertar el tipo de pago'), 400


class RutaAsignaturas(Resource):
    @cross_origin()
    def get(self):
        try:
            asignaturas = session.query(Asignatura).all()
            asignaturas = json.dumps(asignaturas, cls=AlchemyEncoder)
            return {'estado': True, 'mensaje': json.loads(asignaturas)}
        except Exception as e:
            print(e)
            return dict(
                estado=False, detail="Hubo un error al solicitar la lista de asignaturas."), 400

    @cross_origin()
    def post(self):
        asignatura: Asignaturas = request.get_json()
        try:
            asignatura_aux = session.query(Asignatura).filter_by(
                nombre=asignatura['nombre']).first()

            if asignatura_aux:
                return dict(
                    estado=False, detail='La asignatura indicada ya se encuentra en existencia.'), 400

            nueva_asignatura = Asignatura(
                nombre=asignatura['nombre']
            )
            session.add(nueva_asignatura)
            session.commit()
            return {'estado': True, 'mensaje': 'La asignatura se ha agregado con exito.'}
        except Exception as e:
            session.rollback()
            print(e)
            return dict(
                estado=False, detail='Hubo un error al insertar la asignatura'), 400


class RutaCalificaciones(Resource):
    @cross_origin()
    def get(self, numero_matricula: str):
        try:
            alumno: Alumnos = session.query(Alumno).filter_by(
                numero_matricula=numero_matricula).first()

            if not alumno:
                return dict(
                    estado=False, detail="No se encontró el alumno"), 404

            calificacaciones = session.query(
                Calificacion).filter_by(alumno_id=alumno.id).all()
            calificacaciones = json.dumps(calificacaciones, cls=AlchemyEncoder)
            
            return {'estado': True, 'mensaje': json.loads(calificacaciones)}
        except Exception as e:
            print(e)
            return dict(
                estado=False, detail="Hubo un error al solicitar la lista de calificaciones del alumno."), 400
    
    @cross_origin()
    def post(self, numero_matricula: str):
        calificaciones: Calificaciones = request.get_json()
        try:
            alumno: Alumnos = session.query(Alumno).filter_by(
                numero_matricula=numero_matricula).first()

            if not alumno:
                return dict(
                    status=False, detail="No se encontró el alumno."), 404
                
            estado_cuenta: EstadoCuenta = session.query(Pagos).filter_by(alumno_id=alumno.id, asignatura_id=calificaciones['asignatura_id']).first()
            
            if not estado_cuenta:
                return dict(
                    status=False, detail="La asignatura no se ha pagdo."
                )

            calificacion_aux = session.query(Calificacion).filter_by(
                alumno_id=alumno.id, asignatura_id=calificaciones['asignatura_id']).first()

            if calificacion_aux:
                return dict(
                    status=False, detail="La calificacion ya se encuentra registrada."), 400

            nueva_calificacion = Calificacion(
                calificacion=calificaciones['calificacion'],
                asignatura_id=calificaciones['asignatura_id'],
                alumno_id=alumno.id
            )

            session.add(nueva_calificacion)
            session.commit()
            return {'status': True, 'mensaje': 'Calificación/es han registrado con éxito.'}
        except Exception as e:
            print(e)
            session.rollback()
            return dict(
                status=False, detail="Hubo un error al registrar la lista de calificaciones del alumno.")


api.add_resource(RutaEstadosCuenta, '/api/estados_cuenta/<numero_matricula>', '/api/estados_cuenta')
api.add_resource(RutaInstituciones, '/api/instituciones')
api.add_resource(RutaAlumnos, '/api/alumnos')
api.add_resource(RutaTipoPagos, '/api/tipo_pagos')
api.add_resource(RutaAsignaturas, '/api/asignaturas')
api.add_resource(RutaCalificaciones, '/api/calificaciones/<numero_matricula>')

if __name__ == '__main__':
    app.run('0.0.0.0', 8080, debug=True)