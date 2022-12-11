import os
from typing import List
from sqlalchemy import Column, ForeignKey, create_engine
from sqlalchemy.orm import relationship, declarative_base, DeclarativeMeta
from sqlalchemy.types import Integer, String, Float
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()
Base: DeclarativeMeta = declarative_base()

class Asignatura(Base):
    __tablename__ = 'asignaturas'
    id = Column(Integer, primary_key=True)
    nombre = Column(String, nullable=False)
    
    # relacion varios a uno
    calificaciones = relationship('Calificacion')
    
    asignaturas = relationship('Pagos', back_populates='asignatura')
    

class Calificacion(Base):
    __tablename__ = 'calificaciones'
    id = Column(Integer, primary_key=True)
    calificacion = Column(Float, nullable=False)
    alumno_id = Column(Integer)
    asignatura_id = Column(ForeignKey('asignaturas.id'))
    

class TipoPago(Base):
    __tablename__ = 'tipo_pagos'
    id = Column(Integer, primary_key=True)
    tipo_pago = Column(String, nullable=False)
    
    # relacion uno a uno
    pagos = relationship('Pagos', back_populates="tipo_pago")
    

class Institucion(Base):
    __tablename__ = 'instituciones'
    id = Column(Integer, primary_key=True)
    nombre = Column(String, nullable=False)
    
    # relacion uno a uno
    instituciones = relationship('Pagos', back_populates='institucion')


@dataclass
class Alumno(Base):
    __tablename__ = 'alumnos'
    id = Column(Integer, primary_key=True)
    numero_matricula = Column(String(8), nullable=False)
    nombres = Column(String, nullable=False)
    apellidos = Column(String, nullable=False)
    edad = Column(Integer, nullable=False)
    email = Column(String, nullable=False)
    
    # relacion uno a uno
    alumnos = relationship('Pagos', back_populates='alumno')


class Pagos(Base):
    __tablename__ = 'pagos'
    
    id = Column(Integer, primary_key=True)
    
    alumno_id = Column(ForeignKey('alumnos.id'))
    tipo_pago_id = Column(ForeignKey('tipo_pagos.id'))
    institucion_id = Column(ForeignKey('instituciones.id'))
    asignatura_id = Column(ForeignKey('asignaturas.id'))
    
    # relaciones
    alumno = relationship('Alumno', back_populates='alumnos')
    tipo_pago = relationship('TipoPago', back_populates='pagos')
    institucion = relationship('Institucion', back_populates='instituciones')
    asignatura = relationship('Asignatura', back_populates='asignaturas')
    
if __name__ == '__main__':
    engine = create_engine(os.getenv('DATABASE_URL'))
    Base.metadata.create_all(engine)