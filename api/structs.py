from typing import Union
from pydantic import BaseModel

class Alumnos(BaseModel):
    id: Union[int, None]
    numero_matricula: Union[str, None]
    nombres: str
    apellidos: str
    edad: int
    email: str
    

class EstadoCuenta(BaseModel):
    id: Union[int, None]
    numero_matricula: Union[str, None]
    tipo_pago_id: Union[int, None]
    institucion_id: Union[int, None]
    asignatura_id: Union[int, None]
    

class TipoPagos(BaseModel):
    id: Union[int, None]
    tipo_pago: Union[str, None]
    
    
class Instituciones(BaseModel):
    id: Union[int, None]
    nombre: Union[str, None]


class Calificaciones(BaseModel):
    id: Union[int, None]
    calificacion: Union[float, None]
    asignatura_id: Union[int, None]


class Asignaturas(BaseModel):
    id: Union[int, None]
    nombre: Union[str, None]
