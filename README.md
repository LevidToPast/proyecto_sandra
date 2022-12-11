# proyecto_sandra


### Dependencias
 - python 3.7+
 - ruby 3.1.2
 - linux ubuntu 20.04

### Instalacion de rails
para instalar rails seguir los siguientes pasos
```bash
sudo apt update\nsudo apt install gnupg2
gpg2 --keyserver hkp://keyserver.ubuntu.com --recv-keys 409B6B1796C275462A1703113804BB82D39DC0E3 7D2BAF1CF37B13E2069D6956105BD0E739499BDB
\curl -sSL https://get.rvm.io -o rvm.sh
cat rvm.sh | bash -s stable --rails
source ~/.rvm/scripts/rvm
rvm install 3.1.2
gem install rails
cd pagos-client
bundle install
```

### activacion de entorno de trabajo
ya se viene incluida en el repositorio la carpeta venv donde se encuentra todos los modulos que se usaran en los webservices de python
```bash
source venv/bin/activate
```

### Crear base de datos
```bash
cd api
python models.py
```
esto creará una base de datos sqlite3 para el proyecto


### Ejecutar los webservices

#### flask
```bash
cd api
python flask_api.py
```

#### fastapi
```bash
cd api
uvicorn main:app --reload
```

### Ejecutar los clientes

#### flask
```bash
cd flask_client
python app.py
```

#### Rails
```bash
cd pagos_client
rails s
```

## Direcciones
una vez levantadas todos los servicios debereian de encontrarse en las siguientes rutas

- [fastapi] http://localhost:8000/api/* y su 
respectiva ruta ej. alumnos

- [flask cliente] http://localhost:8001/ para entrar al index

- [flask api] http://localhost:8080/api/* y su respectiva ruta

- [rails] http://localhost:3000/registrar_pago