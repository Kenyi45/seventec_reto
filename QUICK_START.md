# 🚀 Guía de Inicio Rápido - EventCorp

## Ejecutar el proyecto en 3 pasos

### 1. Clonar y configurar
```bash
# Clonar el repositorio
git clone <repository-url>
cd seventec

# Crear archivo de configuración
cat > .env << EOF
MONGODB_URL=mongodb://mongodb:27017/eventcorp
MONGODB_DATABASE=eventcorp
SECRET_KEY=your-super-secret-key-here-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
EOF
```

### 2. Ejecutar con Docker
```bash
# Construir y ejecutar todos los servicios
docker-compose up --build

# O en segundo plano
docker-compose up -d --build
```

### 3. Acceder a la aplicación
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **Documentación API**: http://localhost:8000/docs

## 📝 Usuarios de Prueba

### Crear cuenta de Organizador
1. Ir a http://localhost:3000/register
2. Llenar el formulario con:
   - **Nombre**: Tu nombre
   - **Email**: organizador@eventcorp.com
   - **Contraseña**: 123456
   - **Teléfono**: +1234567890
   - **Departamento**: Eventos
   - **Rol**: Organizador

### Crear cuenta de Participante
1. Ir a http://localhost:3000/register
2. Llenar el formulario con:
   - **Nombre**: Tu nombre
   - **Email**: participante@eventcorp.com
   - **Contraseña**: 123456
   - **Teléfono**: +1234567890
   - **Departamento**: Ventas
   - **Rol**: Participante

## 🎯 Funcionalidades a Probar

### Como Organizador
1. **Crear publicación** → Dashboard → "Nueva Publicación"
2. **Crear historia temporal** → Historias → "Nueva Historia"
3. **Gestionar posts** → Editar/Eliminar publicaciones propias

### Como Participante
1. **Ver publicaciones** → Dashboard → Ver lista de eventos
2. **Interactuar** → Dar like y comentar publicaciones
3. **Ver historias** → Sección "Historias"

## 🔧 Comandos Útiles

```bash
# Ver logs del backend
docker-compose logs backend

# Ver logs del frontend
docker-compose logs frontend

# Reiniciar solo el backend
docker-compose restart backend

# Parar todos los servicios
docker-compose down

# Limpiar volúmenes (resetear BD)
docker-compose down -v
```

## 📊 Endpoints API Principales

### Autenticación
- `POST /auth/register` - Registrar usuario
- `POST /auth/login` - Iniciar sesión
- `GET /auth/me` - Obtener usuario actual

### Publicaciones
- `GET /posts` - Listar publicaciones
- `POST /posts` - Crear publicación (solo organizadores)
- `GET /posts/{id}` - Obtener publicación específica
- `POST /posts/{id}/like` - Toggle like
- `POST /posts/{id}/comments` - Agregar comentario

### Historias
- `GET /stories` - Listar historias activas
- `POST /stories` - Crear historia (solo organizadores)
- `POST /stories/{id}/view` - Marcar como vista

## 🐛 Solución de Problemas

### Puerto ocupado
```bash
# Cambiar puertos en docker-compose.yml
# Backend: "8001:8000"
# Frontend: "3001:3000"
```

### Base de datos
```bash
# Resetear base de datos
docker-compose down -v
docker-compose up --build
```

### Dependencias
```bash
# Reconstruir contenedores
docker-compose build --no-cache
docker-compose up
```

## 🌐 Accesos Directos

- [Dashboard](http://localhost:3000)
- [Login](http://localhost:3000/login)
- [Registro](http://localhost:3000/register)
- [API Docs](http://localhost:8000/docs)
- [API Redoc](http://localhost:8000/redoc)

¡Listo! El proyecto debería estar funcionando completamente. 🎉 