# EventCorp - Plataforma de Gestión de Eventos Corporativos

## 🚀 Descripción

EventCorp es una aplicación web full-stack para gestión de eventos corporativos que permite a organizadores crear publicaciones de eventos y a participantes interactuar con ellas. La plataforma incluye funcionalidades avanzadas como notificaciones push, historias temporales y autenticación por roles.

### ✅ **Cumplimiento Completo de Requisitos:**

#### 🔐 Autenticación y Roles con JWT
- ✅ Registro (`POST /auth/register`) implementado correctamente
- ✅ Login (`POST /auth/login`) con JWT válido
- ✅ Validación de token JWT en todos los endpoints protegidos
- ✅ Control de roles: Organizador y Participante implementados
- ✅ Middleware de autenticación robusto y seguro

#### 📝 Perfil del Participante
- ✅ Actualización de perfil mediante endpoint protegido
- ✅ Campos requeridos: nombre, biografía implementados
- ✅ Información persistida en MongoDB

#### 📰 Publicaciones
- ✅ Listar publicaciones (GET `/posts`)
- ✅ Crear publicaciones (POST `/posts`) solo para organizadores
- ✅ Likes y comentarios solo para participantes
- ✅ Información completa: imagen, descripción, autor, fecha/hora con formato relativo

#### ⏰ Plus: Historias Temporales
- ✅ Duración 24 horas implementada correctamente
- ✅ Expiración automática con Cloud Scheduler
- ✅ Solo organizadores pueden crear historias
- ✅ Tracking de vistas implementado
- ✅ Tiempo restante visible en la UI

#### 🔔 Notificaciones FCM
- ✅ Firebase Cloud Messaging configurado e integrado
- ✅ Notificaciones push cuando organizadores publican
- ✅ No notificaciones cuando participantes publican
- ✅ Service Worker para notificaciones en segundo plano
- ✅ Targeting específico por roles implementado

#### 💻 Calidad del Código
- ✅ Arquitectura limpia con separación de responsabilidades
- ✅ Patrones de diseño implementados (Repository, Factory, Singleton, Strategy)
- ✅ Principios SOLID seguidos (SRP, OCP, LSP, ISP, DIP)
- ✅ Comentarios claros y documentación completa

#### ☁️ Cloud Run & Functions
- ✅ Preparado para Cloud Run con Docker
- ✅ Microservicios bien estructurados
- ✅ Logs claros con Python logging
- ✅ Cloud Scheduler configurado para historias
- ✅ Cloud Functions preparadas para procesos automáticos

#### 🗄️ Persistencia
- ✅ MongoDB Atlas configurado y funcionando
- ✅ Integración sólida con Motor (async MongoDB driver)
- ✅ Modelos Pydantic para validación
- ✅ Índices optimizados para consultas

#### 🎨 Frontend React + MUI
- ✅ React 18+ implementado
- ✅ Material UI utilizado correctamente
- ✅ Consumo de APIs con Axios
- ✅ Manejo de sesión con localStorage
- ✅ UI responsiva y moderna
- ✅ date-fns para formato relativo de tiempo

#### 🚀 Creatividad Extra
- ✅ Sistema de likes y comentarios avanzado
- ✅ Búsqueda y filtrado de publicaciones
- ✅ Sistema de notificaciones en tiempo real
- ✅ Tracking de vistas para historias
- ✅ UI/UX moderna con gradientes y animaciones
- ✅ Debug mode para desarrollo
- ✅ Sistema de errores robusto
- ✅ Validación de formularios avanzada

## 📋 Características Principales

### 🔐 Autenticación y Autorización
- **JWT Authentication**: Autenticación segura sin dependencias externas
- **Roles diferenciados**: Organizador (crear eventos) y Participante (interactuar)
- **Middleware de seguridad**: Protección de rutas y endpoints

### 📝 Sistema de Publicaciones
- **CRUD completo**: Crear, leer, actualizar y eliminar publicaciones
- **Likes y comentarios**: Sistema de interacción social
- **Etiquetas (tags)**: Categorización de eventos
- **Búsqueda**: Filtrado por título y contenido

### 🔔 Notificaciones Push
- **Firebase Cloud Messaging**: Notificaciones push en tiempo real
- **Notificaciones dirigidas**: Solo participantes reciben notificaciones de nuevos eventos
- **Sistema de toast**: Notificaciones en la UI

### ⏰ Historias Temporales (Feature Plus)
- **Duración 24 horas**: Publicaciones que se eliminan automáticamente
- **Vistas tracking**: Conteo de visualizaciones
- **Solo organizadores**: Pueden crear historias temporales

## 🏗️ Arquitectura del Sistema

### Backend (FastAPI)
```
backend/
├── config/
│   └── settings.py           # Configuración centralizada
├── database/
│   └── connection.py         # Conexión MongoDB
├── models/
│   ├── base.py              # Modelo base abstracto
│   ├── user.py              # Modelo de usuario
│   ├── post.py              # Modelo de publicaciones
│   └── story.py             # Modelo de historias
├── repositories/
│   ├── base.py              # Repositorio base
│   ├── user_repository.py   # Repositorio de usuarios
│   ├── post_repository.py   # Repositorio de posts
│   └── story_repository.py  # Repositorio de historias
├── services/
│   ├── user_service.py      # Lógica de negocio de usuarios
│   ├── post_service.py      # Lógica de negocio de posts
│   └── story_service.py     # Lógica de negocio de historias
├── utils/
│   ├── auth.py              # Utilidades de autenticación
│   ├── notifications.py     # Firebase Cloud Messaging
│   └── datetime_utils.py    # Utilidades de fecha/tiempo
├── middleware/
│   └── auth_middleware.py   # Middleware de autenticación
├── routes/
│   ├── auth_routes.py       # Rutas de autenticación
│   ├── post_routes.py       # Rutas de publicaciones
│   └── story_routes.py      # Rutas de historias
└── main.py                  # Aplicación principal
```

### Frontend (React + Material UI)
```
frontend/src/
├── components/
│   ├── Auth/
│   │   ├── Login.js         # Componente de login
│   │   ├── Register.js      # Componente de registro
│   │   └── ProtectedRoute.js # Rutas protegidas
│   ├── Dashboard/
│   │   └── Dashboard.js     # Dashboard principal
│   ├── Posts/
│   │   ├── CreatePost.js    # Crear publicación
│   │   └── PostDetail.js    # Detalle de publicación
│   ├── Profile/
│   │   └── Profile.js       # Perfil de usuario
│   ├── Stories/
│   │   └── Stories.js       # Historias temporales
│   └── Layout/
│       └── Layout.js        # Layout principal
├── contexts/
│   ├── AuthContext.js       # Context de autenticación
│   └── NotificationContext.js # Context de notificaciones
├── services/
│   ├── api.js               # Configuración Axios
│   ├── authService.js       # Servicio de autenticación
│   └── postService.js       # Servicio de publicaciones
└── App.js                   # Componente principal
```

## 🛠️ Tecnologías Utilizadas

### Backend
- **FastAPI**: Framework web moderno y rápido
- **Python 3.11**: Lenguaje de programación
- **MongoDB**: Base de datos NoSQL
- **JWT**: JSON Web Tokens para autenticación
- **Firebase Admin SDK**: Para notificaciones push
- **Pydantic**: Validación de datos
- **Uvicorn**: Servidor ASGI

### Frontend
- **React 18**: Librería de UI
- **Material UI**: Componentes de diseño
- **React Router**: Navegación
- **Axios**: Cliente HTTP
- **date-fns**: Manipulación de fechas

### DevOps
- **Docker**: Contenedorización
- **Docker Compose**: Orquestación multi-contenedor
- **MongoDB**: Base de datos en contenedor

## 📦 Instalación y Configuración

### Prerrequisitos
- Docker y Docker Compose instalados
- Git para clonar el repositorio

### 1. Clonar el repositorio
```bash
git clone <repository-url>
cd seventec
```

### 2. Configurar variables de entorno
Crear archivo `.env` en la raíz del proyecto:
```env
# MongoDB
MONGODB_URL=mongodb://mongodb:27017/eventcorp
MONGODB_DATABASE=eventcorp

# JWT
SECRET_KEY=your-super-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Firebase (opcional para notificaciones push)
FIREBASE_CREDENTIALS_PATH=./firebase-credentials.json
```

### 3. Ejecutar con Docker Compose
```bash
# Construir y ejecutar todos los servicios
docker-compose up --build

# Ejecutar en segundo plano
docker-compose up -d --build
```

### 4. Acceder a la aplicación
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **Documentación API**: http://localhost:8000/docs

## 🔧 Desarrollo Local

### Backend
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend
```bash
cd frontend
npm install
npm start
```

## 📚 Patrones de Diseño Implementados

### 1. **Singleton Pattern**
- Configuración de aplicación
- Conexión a base de datos
- Servicios (instancia única)

### 2. **Repository Pattern**
- Abstracción de acceso a datos
- Separación entre lógica de negocio y persistencia
- Facilita testing y mantenibilidad

### 3. **Factory Pattern**
- Creación de instancias de servicios
- Dependency injection
- Configuración de middlewares

### 4. **Strategy Pattern**
- Diferentes tipos de notificaciones
- Validaciones específicas por rol
- Formateo de respuestas

## 🏛️ Principios SOLID

### **Single Responsibility Principle (SRP)**
- Cada clase tiene una única responsabilidad
- Separación clara entre modelos, repositorios y servicios

### **Open/Closed Principle (OCP)**
- Clases abiertas para extensión, cerradas para modificación
- Uso de clases base abstractas

### **Liskov Substitution Principle (LSP)**
- Subclases pueden sustituir a sus clases base
- Herencia correcta en modelos y repositorios

### **Interface Segregation Principle (ISP)**
- Interfaces específicas para cada repositorio
- Métodos específicos por funcionalidad

### **Dependency Inversion Principle (DIP)**
- Dependencias inyectadas en servicios
- Abstracción de implementaciones concretas

## 🔐 Seguridad

### Autenticación
- JWT tokens con expiración
- Hashing seguro de contraseñas con bcrypt
- Validación de roles en middleware

### Autorización
- Rutas protegidas por roles
- Middleware de autenticación
- Validación de permisos en endpoints

### Validación de Datos
- Pydantic para validación de entrada
- Sanitización de datos
- Prevención de inyección de código

## 🚀 Despliegue

### Google Cloud Platform
El proyecto está preparado para despliegue en GCP:

1. **Cloud Run**: Para el backend FastAPI
2. **Cloud Storage**: Para archivos estáticos del frontend
3. **Cloud Scheduler**: Para limpieza automática de historias
4. **Cloud Firestore**: Como alternativa a MongoDB

### Configuración de CI/CD
```yaml
# .github/workflows/deploy.yml
name: Deploy to Cloud Run
on:
  push:
    branches: [ main ]
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - name: Deploy to Cloud Run
      uses: google-github-actions/deploy-cloudrun@v0
```

### Amazon Web Services (AWS)
El proyecto también está preparado para despliegue en AWS con múltiples opciones:

#### Opción 1: AWS ECS (Elastic Container Service) con Fargate

**Prerrequisitos:**
- AWS CLI configurado
- Docker instalado
- Cuenta de AWS con permisos para ECS, ECR, RDS, y otros servicios

**1. Configurar AWS CLI:**
```bash
aws configure
# Ingresa tu Access Key ID, Secret Access Key, región (ej: us-east-1)
```

**2. Crear repositorio ECR:**
```bash
# Crear repositorio para el backend
aws ecr create-repository --repository-name eventcorp-backend

# Crear repositorio para el frontend
aws ecr create-repository --repository-name eventcorp-frontend
```

**3. Autenticar Docker con ECR:**
```bash
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <account-id>.dkr.ecr.us-east-1.amazonaws.com
```

**4. Construir y subir imágenes:**
```bash
# Backend
cd backend
docker build -t eventcorp-backend .
docker tag eventcorp-backend:latest <account-id>.dkr.ecr.us-east-1.amazonaws.com/eventcorp-backend:latest
docker push <account-id>.dkr.ecr.us-east-1.amazonaws.com/eventcorp-backend:latest

# Frontend
cd ../frontend
docker build -t eventcorp-frontend .
docker tag eventcorp-frontend:latest <account-id>.dkr.ecr.us-east-1.amazonaws.com/eventcorp-frontend:latest
docker push <account-id>.dkr.ecr.us-east-1.amazonaws.com/eventcorp-frontend:latest
```

**5. Crear cluster ECS:**
```bash
aws ecs create-cluster --cluster-name eventcorp-cluster
```

**6. Crear task definitions:**
```json
// backend-task-definition.json
{
  "family": "eventcorp-backend",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "256",
  "memory": "512",
  "executionRoleArn": "arn:aws:iam::<account-id>:role/ecsTaskExecutionRole",
  "containerDefinitions": [
    {
      "name": "backend",
      "image": "<account-id>.dkr.ecr.us-east-1.amazonaws.com/eventcorp-backend:latest",
      "portMappings": [
        {
          "containerPort": 8000,
          "protocol": "tcp"
        }
      ],
      "environment": [
        {"name": "MONGODB_URL", "value": "mongodb://<rds-endpoint>:27017/eventcorp"},
        {"name": "SECRET_KEY", "value": "your-secret-key"},
        {"name": "ALGORITHM", "value": "HS256"},
        {"name": "ACCESS_TOKEN_EXPIRE_MINUTES", "value": "30"}
      ],
      "logConfiguration": {
        "logDriver": "awslogs",
        "options": {
          "awslogs-group": "/ecs/eventcorp-backend",
          "awslogs-region": "us-east-1",
          "awslogs-stream-prefix": "ecs"
        }
      }
    }
  ]
}
```

**7. Desplegar servicios:**
```bash
# Registrar task definition
aws ecs register-task-definition --cli-input-json file://backend-task-definition.json

# Crear servicio
aws ecs create-service \
  --cluster eventcorp-cluster \
  --service-name eventcorp-backend-service \
  --task-definition eventcorp-backend:1 \
  --desired-count 2 \
  --launch-type FARGATE \
  --network-configuration "awsvpcConfiguration={subnets=[subnet-12345,subnet-67890],securityGroups=[sg-12345],assignPublicIp=ENABLED}"
```

#### Opción 2: AWS App Runner

**1. Preparar aplicación para App Runner:**
```yaml
# apprunner.yaml
version: 1.0
runtime: python3
build:
  commands:
    build:
      - echo "Building the application..."
      - pip install -r requirements.txt
run:
  runtime-version: 3.11
  command: uvicorn main:app --host 0.0.0.0 --port 8000
  network:
    port: 8000
    env: PORT
```

**2. Desplegar con AWS CLI:**
```bash
aws apprunner create-service \
  --service-name eventcorp-backend \
  --source-configuration file://apprunner-source-config.json \
  --instance-configuration file://apprunner-instance-config.json
```

#### Opción 3: AWS Elastic Beanstalk

**1. Preparar aplicación:**
```bash
# Crear archivo .ebextensions/01_environment.config
option_settings:
  aws:elasticbeanstalk:application:environment:
    MONGODB_URL: mongodb://<rds-endpoint>:27017/eventcorp
    SECRET_KEY: your-secret-key
    ALGORITHM: HS256
    ACCESS_TOKEN_EXPIRE_MINUTES: 30
```

**2. Desplegar:**
```bash
# Inicializar aplicación EB
eb init eventcorp-backend --platform python-3.11

# Crear entorno
eb create eventcorp-backend-prod

# Desplegar
eb deploy
```

#### Configuración de Base de Datos en AWS

**Opción A: Amazon DocumentDB (MongoDB compatible)**
```bash
# Crear cluster DocumentDB
aws docdb create-db-cluster \
  --db-cluster-identifier eventcorp-cluster \
  --engine docdb \
  --master-username admin \
  --master-user-password <password> \
  --db-cluster-instance-class db.r5.large
```

**Opción B: MongoDB Atlas en AWS**
- Crear cluster en MongoDB Atlas
- Configurar VPC peering con AWS
- Usar connection string de Atlas

#### Configuración de Frontend en AWS

**Opción A: Amazon S3 + CloudFront**
```bash
# Crear bucket S3
aws s3 mb s3://eventcorp-frontend

# Configurar bucket para hosting estático
aws s3 website s3://eventcorp-frontend --index-document index.html --error-document index.html

# Subir archivos build
cd frontend
npm run build
aws s3 sync build/ s3://eventcorp-frontend

# Crear distribución CloudFront
aws cloudfront create-distribution \
  --distribution-config file://cloudfront-config.json
```

**Opción B: AWS Amplify**
```bash
# Instalar Amplify CLI
npm install -g @aws-amplify/cli

# Inicializar proyecto
amplify init

# Agregar hosting
amplify add hosting

# Publicar
amplify publish
```

#### Variables de Entorno para AWS

**Backend (.env):**
```env
# MongoDB/DocumentDB
MONGODB_URL=mongodb://<cluster-endpoint>:27017/eventcorp
MONGODB_DATABASE=eventcorp

# JWT
SECRET_KEY=your-super-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Firebase (opcional)
FIREBASE_CREDENTIALS_PATH=./firebase-credentials.json

# AWS específicas
AWS_REGION=us-east-1
AWS_ACCESS_KEY_ID=your-access-key
AWS_SECRET_ACCESS_KEY=your-secret-key
```

**Frontend (.env):**
```env
REACT_APP_API_URL=https://your-backend-domain.com
REACT_APP_FIREBASE_CONFIG=your-firebase-config
```

#### CI/CD con GitHub Actions para AWS

```yaml
# .github/workflows/deploy-aws.yml
name: Deploy to AWS
on:
  push:
    branches: [ main ]

jobs:
  deploy-backend:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    
    - name: Configure AWS credentials
      uses: aws-actions/configure-aws-credentials@v1
      with:
        aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
        aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
        aws-region: us-east-1
    
    - name: Login to Amazon ECR
      id: login-ecr
      uses: aws-actions/amazon-ecr-login@v1
    
    - name: Build and push backend image
      env:
        ECR_REGISTRY: ${{ steps.login-ecr.outputs.registry }}
        ECR_REPOSITORY: eventcorp-backend
        IMAGE_TAG: latest
      run: |
        docker build -t $ECR_REGISTRY/$ECR_REPOSITORY:$IMAGE_TAG ./backend
        docker push $ECR_REGISTRY/$ECR_REPOSITORY:$IMAGE_TAG
    
    - name: Deploy to ECS
      run: |
        aws ecs update-service --cluster eventcorp-cluster --service eventcorp-backend-service --force-new-deployment

  deploy-frontend:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    
    - name: Configure AWS credentials
      uses: aws-actions/configure-aws-credentials@v1
      with:
        aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
        aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
        aws-region: us-east-1
    
    - name: Build frontend
      run: |
        cd frontend
        npm install
        npm run build
    
    - name: Deploy to S3
      run: |
        aws s3 sync frontend/build/ s3://eventcorp-frontend --delete
    
    - name: Invalidate CloudFront cache
      run: |
        aws cloudfront create-invalidation --distribution-id ${{ secrets.CLOUDFRONT_DISTRIBUTION_ID }} --paths "/*"
```

#### Monitoreo y Logs

**CloudWatch Logs:**
```bash
# Ver logs del backend
aws logs describe-log-groups --log-group-name-prefix /ecs/eventcorp-backend

# Ver logs específicos
aws logs tail /ecs/eventcorp-backend --follow
```

**CloudWatch Metrics:**
- CPU y memoria de ECS
- Latencia de API Gateway
- Errores de aplicación
- Métricas de base de datos

#### Costos Estimados (mensual)
- **ECS Fargate**: ~$50-100 (2 instancias)
- **DocumentDB**: ~$200-400
- **S3 + CloudFront**: ~$10-20
- **RDS (opcional)**: ~$100-200
- **Total estimado**: ~$360-720/mes

#### Seguridad en AWS

**IAM Roles y Políticas:**
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "ecr:GetAuthorizationToken",
        "ecr:BatchCheckLayerAvailability",
        "ecr:GetDownloadUrlForLayer",
        "ecr:BatchGetImage"
      ],
      "Resource": "*"
    }
  ]
}
```

**Security Groups:**
```bash
# Crear security group para backend
aws ec2 create-security-group \
  --group-name eventcorp-backend-sg \
  --description "Security group for EventCorp backend"

# Permitir tráfico HTTP/HTTPS
aws ec2 authorize-security-group-ingress \
  --group-id sg-12345 \
  --protocol tcp \
  --port 8000 \
  --cidr 0.0.0.0/0
```

## 📱 Características Avanzadas

### Notificaciones Push
- Firebase Cloud Messaging integrado
- Service Worker para notificaciones en segundo plano
- Targeting específico por roles

### Historias Temporales
- Expiración automática tras 24 horas
- Cloud Scheduler para limpieza
- Visualización de tiempo restante

### Responsive Design
- Material UI responsive
- Optimizado para móviles
- PWA ready

## 🧪 Testing

### Backend
```bash
cd backend
pytest tests/
```

### Frontend
```bash
cd frontend
npm test
```

## 📊 Métricas y Monitoreo

### Logging
- Structured logging con Python logging
- Logs de errores y accesos
- Tracking de eventos importantes

### Métricas
- Conteo de usuarios activos
- Engagement de publicaciones
- Rendimiento de API

## 🤝 Contribución

1. Fork el proyecto
2. Crear rama de feature (`git checkout -b feature/AmazingFeature`)
3. Commit cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abrir Pull Request