import os
import random
from typing import Dict, List, Union
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from pydantic import BaseModel
from dotenv import load_dotenv

from models import Alumno, Pagos, Institucion, TipoPago, Asignatura, Calificacion
from structs import Alumnos, EstadoCuenta, Instituciones, TipoPagos, Calificaciones, Asignaturas

# Cargar todas las variables de entorno al código
load_dotenv()

# Crear engine para la base de datos
engine = create_engine(os.getenv('DATABASE_URL'))

# Crear sesion para conectarser a la base de datos
session: Session = sessionmaker(bind=engine)()

# Crear aplicación de Fast Api
app = FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rutas de Api


@app.get("/api/estados_cuenta/{numero_matricula}")
async def mostrar_estadosCuenta(numero_matricula: str):
    alumno: Alumno = session.query(Alumno).filter_by(
        numero_matricula=numero_matricula).first()

    if not alumno:
        raise HTTPException(
            status_code=404, detail='No se encontró el alumno.')

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


@app.post("/api/estados_cuenta")
async def agregar_estadosCuenta(pago: EstadoCuenta):
    try:
        alumno: Alumno = session.query(Alumno).filter_by(
            numero_matricula=pago.numero_matricula).first()
        
        if not alumno:
            raise HTTPException(status_code=404, detail='Alumno solicidado no encontrado.')

        estado_cuenta = session.query(Pagos).filter_by(alumno_id=alumno.id, asignatura_id=pago.asignatura_id)
        
        if estado_cuenta:
            raise HTTPException(status_code=400, detail='Pago solicitado ya ha sido registradp con anterioridad.')

        nuevo_pago = Pagos(
            alumno_id=alumno.id,
            tipo_pago_id=pago.tipo_pago_id,
            institucion_id=pago.institucion_id,
            asignatura_id=pago.asignatura_id
        )
        session.add(nuevo_pago)
        session.commit()
        return {'estado': True, "mensaje": 'Pago registrado con éxito'}
    except Exception as e:
        print(e)
        session.rollback()
        raise HTTPException(
            status_code=400, detail='Hubo un error al insertar el pago.')


@app.get("/api/instituciones")
async def mostrar_instituciones():
    try:
        institucion = session.query(Institucion).all()
        return {'estado': True, 'mensaje': institucion}
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=400, detail="Hubo un error al solicitar la lista de instituciones.")


@app.post("/api/instituciones")
async def agregar_institucion(institucion: Instituciones):
    institucion_aux = session.query(Institucion).filter_by(
        nombre=institucion.nombre).first()

    if institucion_aux:
        raise HTTPException(
            status_code=400, detail='Institucion solicitada ya se encuentra en existencia')

    try:
        nueva_institucion = Institucion(
            nombre=institucion.nombre
        )
        session.add(nueva_institucion)
        session.commit()
        return {'estado': True, 'mensaje': 'La institución se ha agregado con exito.'}
    except Exception as e:
        session.rollback()
        print(e)
        raise HTTPException(
            status_code=400, detail='Hubo un error al insertar la institución')


@app.get("/api/alumnos")
async def mostrar_alumnos():
    try:
        alumnos = session.query(Alumno).all()
        return {'estado': True, 'mensaje': alumnos}
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=400, detail="Hubo un error al solicitar la lista de alumnos.")


@app.post("/api/alumnos")
async def agregar_usuario(alumno: Alumnos):
    try:
        # genera una cadena random de 8 numeros
        numero_cuenta = str(random.randint(10000000, 99999999))
        nuevo_alumno = Alumno(
            numero_matricula=numero_cuenta,
            nombres=alumno.nombres,
            apellidos=alumno.apellidos,
            edad=alumno.edad,
            email=alumno.email
        )
        session.add(nuevo_alumno)
        session.commit()
        return {'estado': True, 'mensaje': 'El alumno se ha agregado con exito.'}
    except Exception as e:
        session.rollback()
        print(e)
        raise HTTPException(
            status_code=400, detail='Hubo un error al insertar el alumno')


@app.get("/api/tipo_pagos")
async def mostrar_tipos_pagos():
    try:
        tipos_pagos = session.query(TipoPago).all()
        return {'estado': True, 'mensaje': tipos_pagos}
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=400, detail="Hubo un error al solicitar la lista de tipo de pagos.")


@app.post("/api/tipo_pagos")
async def agregar_tipo_pago(tipo_pago: TipoPagos):
    try:
        nuevo_tipo_pago = TipoPago(
            tipo_pago=tipo_pago.tipo_pago
        )
        session.add(nuevo_tipo_pago)
        session.commit()
        return {'estado': True, 'mensaje': 'El tipo de pago se ha agregado con exito.'}
    except Exception as e:
        print(e)
        session.rollback()
        raise HTTPException(
            status_code=400, detail='Hubo un error al insertar el tipo de pago')


@app.get("/api/asignaturas")
async def mostrar_asignaturas():
    try:
        asignaturas = session.query(Asignatura).all()
        return {'estado': True, 'mensaje': asignaturas}
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=400, detail="Hubo un error al solicitar la lista de asignaturas.")


@app.post("/api/asignaturas")
async def agregar_asignatura(asignatura: Asignaturas):
    try:
        asignatura_aux = session.query(Asignatura).filter_by(
            nombre=asignatura.nombre).first()

        if asignatura_aux:
            raise HTTPException(
                status_code=400, detail='La asignatura indicada ya se encuentra en existencia.')

        nueva_asignatura = Asignatura(
            nombre=asignatura.nombre
        )
        session.add(nueva_asignatura)
        session.commit()
        return {'estado': True, 'mensaje': 'La asignatura se ha agregado con exito.'}
    except Exception as e:
        session.rollback()
        print(e)
        raise HTTPException(
            status_code=400, detail='Hubo un error al insertar la asignatura')


@app.get("/api/calificaciones/{numero_matricula}")
async def mostrar_calificaciones(numero_matricula: str):
    try:
        alumno: Alumnos = session.query(Alumno).filter_by(
            numero_matricula=numero_matricula).first()

        if not alumno:
            raise HTTPException(
                status_code=404, detail="No se encontró el alumno")

        calificacaciones = session.query(
            Calificacion).filter_by(alumno_id=alumno.id).all()

        return {'estado': True, 'mensaje': calificacaciones}
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=400, detail="Hubo un error al solicitar la lista de calificaciones del alumno.")


@app.post("/api/calificaciones/{numero_matricula}")
async def agregar_calificaciones(numero_matricula: str, calificaciones: Calificaciones):
    try:
        alumno: Alumnos = session.query(Alumno).filter_by(
            numero_matricula=numero_matricula).first()

        if not alumno:
            raise HTTPException(
                status_code=404, detail="No se encontró el alumno.")

        estado_cuenta = session.query(Pagos).filter_by(alumno_id=alumno.id, asignatura_id=calificaciones.asignatura_id).first()
        
        if not estado_cuenta:
            raise HTTPException(400, "La asignatura no se ha pagado")

        calificacion_aux = session.query(Calificacion).filter_by(
            alumno_id=alumno.id, asignatura_id=calificaciones.asignatura_id).first()

        if calificacion_aux:
            raise HTTPException(
                status_code=400, detail="La calificacion ya se encuentra registrada.")

        nueva_calificacion = Calificacion(
            calificacion=calificaciones.calificacion,
            asignatura_id=calificaciones.asignatura_id,
            alumno_id=alumno.id
        )

        session.add(nueva_calificacion)
        session.commit()
        return {'status': True, 'mensaje': 'Calificación/es han registrado con éxito.'}
    except Exception as e:
        print(e)
        session.rollback()
        raise HTTPException(
            status_code=400, detail="Hubo un error al registrar la lista de calificaciones del alumno.")
