# 🎬 Guía de Demostración - EventCorp

## 🚀 Demo Completo del Proyecto

Esta guía te ayudará a realizar una demostración completa de todas las funcionalidades de EventCorp.

---

## 📋 Preparación del Demo

### 1. Iniciar el Proyecto
```bash
# Clonar el repositorio (si no lo tienes)
git clone <repository-url>
cd seventec

# Iniciar todos los servicios
docker-compose up -d --build

# Verificar que todos los servicios estén corriendo
docker-compose ps
```

### 2. Verificar Acceso
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **Documentación API**: http://localhost:8000/docs

---

## 🎭 Script de Demostración

### **Paso 1: Registro de Usuarios** 👥

#### 1.1 Crear Organizador
1. Ir a http://localhost:3000/register
2. Llenar formulario:
   - **Nombre**: "Ana Organizadora"
   - **Email**: "ana@eventcorp.com"
   - **Contraseña**: "password123"
   - **Rol**: "Organizador"
3. Hacer clic en "Crear Cuenta"
4. **Resultado esperado**: Redirección automática al dashboard

#### 1.2 Crear Participante
1. Ir a http://localhost:3000/register
2. Llenar formulario:
   - **Nombre**: "Carlos Participante"
   - **Email**: "carlos@eventcorp.com"
   - **Contraseña**: "password123"
   - **Rol**: "Participante"
3. Hacer clic en "Crear Cuenta"
4. **Resultado esperado**: Redirección automática al dashboard

---

### **Paso 2: Funcionalidades del Organizador** 🎯

#### 2.1 Crear Publicación
1. Iniciar sesión como Ana Organizadora
2. En el dashboard, hacer clic en "Crear Publicación"
3. Llenar formulario:
   - **Título**: "Bienvenidos al Evento Corporativo 2025"
   - **Contenido**: "Estamos emocionados de darles la bienvenida a nuestro evento anual. Tendremos charlas inspiradoras, networking y muchas sorpresas."
   - **URL de imagen**: "https://images.unsplash.com/photo-1540575467063-178a50c2df87?w=800"
   - **Etiquetas**: "evento, corporativo, networking"
4. Hacer clic en "Crear Publicación"
5. **Resultado esperado**: Publicación creada y visible en el feed

#### 2.2 Crear Historia Temporal
1. En el dashboard, hacer clic en "Historias" en el menú
2. Hacer clic en "Nueva Historia"
3. Llenar formulario:
   - **Contenido**: "¡Recordatorio! El evento comienza en 2 horas. ¡No se lo pierdan!"
   - **URL de imagen**: "https://images.unsplash.com/photo-1511795409834-ef04bbd61622?w=800"
4. Hacer clic en "Crear Historia"
5. **Resultado esperado**: Historia creada con contador de 24 horas

#### 2.3 Ver Estadísticas
1. En el dashboard, verificar que aparecen:
   - Contador de publicaciones creadas
   - Contador de historias activas
   - Información del perfil

---

### **Paso 3: Funcionalidades del Participante** 👤

#### 3.1 Ver Contenido
1. Cerrar sesión y iniciar como Carlos Participante
2. En el dashboard, verificar que aparecen:
   - Publicaciones creadas por organizadores
   - Historias temporales activas
   - **Nota**: No debe aparecer botón "Crear Publicación"

#### 3.2 Interactuar con Publicaciones
1. En una publicación, hacer clic en "Me gusta"
2. **Resultado esperado**: Contador de likes aumenta
3. Hacer clic en "Comentar"
4. Escribir: "¡Excelente iniciativa! Estoy muy emocionado por participar."
5. Hacer clic en "Enviar Comentario"
6. **Resultado esperado**: Comentario aparece en la publicación

#### 3.3 Ver Historia Completa
1. En la sección de historias, hacer clic en "Ver historia completa"
2. **Resultado esperado**: Modal con contenido completo y tiempo restante
3. Cerrar modal y verificar que el contador de vistas aumentó

#### 3.4 Editar Perfil
1. En el menú, hacer clic en "Perfil"
2. Editar información:
   - **Biografía**: "Desarrollador apasionado por la innovación tecnológica"
   - **Alergias**: "Ninguna"
3. Hacer clic en "Guardar Cambios"
4. **Resultado esperado**: Perfil actualizado

---

### **Paso 4: Funcionalidades Avanzadas** 🔥

#### 4.1 Búsqueda de Publicaciones
1. En el dashboard, usar la barra de búsqueda
2. Buscar "evento"
3. **Resultado esperado**: Filtrado de publicaciones que contengan "evento"

#### 4.2 Ver Detalle de Publicación
1. Hacer clic en una publicación
2. **Resultado esperado**: Página de detalle con:
   - Información completa
   - Lista de comentarios
   - Lista de likes
   - Botones de interacción

#### 4.3 Navegación Responsiva
1. Redimensionar la ventana del navegador
2. **Resultado esperado**: La interfaz se adapta correctamente
3. Probar en modo móvil (F12 → Device Toolbar)

---

### **Paso 5: Notificaciones y Tiempo Real** 🔔

#### 5.1 Simular Notificaciones
1. En otra pestaña, iniciar sesión como Ana Organizadora
2. Crear una nueva publicación
3. Volver a la pestaña de Carlos Participante
4. **Resultado esperado**: Notificación toast aparece

#### 5.2 Verificar Historias Temporales
1. En la sección de historias, verificar:
   - Contador de tiempo restante
   - Estado activo/inactivo
   - Contador de vistas

---

## 🎯 Puntos Clave a Destacar

### **1. Arquitectura Sólida**
- ✅ Separación clara entre frontend y backend
- ✅ Patrones de diseño implementados
- ✅ Código limpio y mantenible

### **2. Seguridad**
- ✅ Autenticación JWT sin dependencias externas
- ✅ Control de roles implementado
- ✅ Validación de datos en frontend y backend

### **3. Funcionalidades Avanzadas**
- ✅ Historias temporales con expiración automática
- ✅ Sistema de notificaciones push
- ✅ Interacciones sociales (likes, comentarios)
- ✅ UI/UX moderna y responsiva

### **4. Escalabilidad**
- ✅ Preparado para Cloud Run
- ✅ Base de datos MongoDB escalable
- ✅ Microservicios bien estructurados

---

## 🛠️ Comandos Útiles para el Demo

### Verificar Estado de Servicios
```bash
# Ver logs en tiempo real
docker-compose logs -f

# Ver logs específicos
docker-compose logs backend
docker-compose logs frontend

# Verificar estado de contenedores
docker-compose ps
```

### Reiniciar Servicios
```bash
# Reiniciar todo
docker-compose restart

# Reiniciar servicio específico
docker-compose restart backend
docker-compose restart frontend
```

### Limpiar y Reconstruir
```bash
# Limpiar todo y reconstruir
docker-compose down
docker-compose up -d --build
```

---

## 🎬 Script de Presentación

### **Introducción (2 min)**
"EventCorp es una plataforma moderna para gestión de eventos corporativos que conecta organizadores y participantes a través de una experiencia tipo Instagram/TikTok."

### **Demo de Registro (3 min)**
"Primero, vamos a crear dos tipos de usuarios: un organizador y un participante, mostrando el sistema de roles."

### **Funcionalidades del Organizador (5 min)**
"Como organizador, puedo crear publicaciones permanentes e historias temporales que se eliminan automáticamente tras 24 horas."

### **Funcionalidades del Participante (5 min)**
"Como participante, puedo interactuar con el contenido, dar likes, comentar y editar mi perfil."

### **Características Avanzadas (3 min)**
"La plataforma incluye búsqueda, notificaciones push, y una interfaz completamente responsiva."

### **Cierre (2 min)**
"EventCorp demuestra las mejores prácticas de desarrollo fullstack moderno, con arquitectura escalable y código de alta calidad."

---

## 🚨 Solución de Problemas

### Si el frontend no carga:
```bash
docker-compose logs frontend
# Verificar que el puerto 3000 esté disponible
```

### Si el backend no responde:
```bash
docker-compose logs backend
# Verificar conexión a MongoDB
```

### Si las notificaciones no funcionan:
- Verificar configuración de Firebase
- Revisar logs del backend para errores de FCM

### Si las historias no expiran:
- Verificar que el scheduler esté configurado
- Revisar logs del backend

---

## 📊 Métricas de Éxito del Demo

- ✅ **Tiempo total**: 20-25 minutos
- ✅ **Interacciones del público**: 3-5 preguntas
- ✅ **Funcionalidades mostradas**: 100%
- ✅ **Tecnologías destacadas**: Todas las requeridas
- ✅ **Calidad del código**: Visible en la estructura

---

**¡Listo para una demostración exitosa!** 🎉 