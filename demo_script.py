#!/usr/bin/env python3
"""
Script de Demostración Automatizada - EventCorp
Este script ayuda a preparar y ejecutar una demostración completa del proyecto.
"""

import requests
import json
import time
import subprocess
import sys
from datetime import datetime

class EventCorpDemo:
    def __init__(self):
        self.base_url = "http://localhost:8000/api/v1"
        self.frontend_url = "http://localhost:3000"
        self.session = requests.Session()
        
    def print_header(self, title):
        """Imprimir encabezado con formato"""
        print("\n" + "="*60)
        print(f"🎬 {title}")
        print("="*60)
    
    def print_step(self, step, description):
        """Imprimir paso de la demostración"""
        print(f"\n📋 Paso {step}: {description}")
        print("-" * 40)
    
    def check_services(self):
        """Verificar que los servicios estén corriendo"""
        self.print_header("Verificación de Servicios")
        
        try:
            # Verificar backend
            response = requests.get(f"{self.base_url}/health", timeout=5)
            if response.status_code == 200:
                print("✅ Backend API: Funcionando")
            else:
                print("❌ Backend API: Error")
                return False
        except requests.exceptions.RequestException:
            print("❌ Backend API: No disponible")
            return False
        
        try:
            # Verificar frontend
            response = requests.get(self.frontend_url, timeout=5)
            if response.status_code == 200:
                print("✅ Frontend: Funcionando")
            else:
                print("❌ Frontend: Error")
                return False
        except requests.exceptions.RequestException:
            print("❌ Frontend: No disponible")
            return False
        
        try:
            # Verificar MongoDB
            response = requests.get(f"{self.base_url}/health/db", timeout=5)
            if response.status_code == 200:
                print("✅ Base de Datos: Funcionando")
            else:
                print("❌ Base de Datos: Error")
                return False
        except requests.exceptions.RequestException:
            print("❌ Base de Datos: No disponible")
            return False
        
        return True
    
    def create_test_users(self):
        """Crear usuarios de prueba para la demostración"""
        self.print_header("Creación de Usuarios de Prueba")
        
        users = [
            {
                "full_name": "Ana Organizadora",
                "email": "ana@eventcorp.com",
                "password": "password123",
                "role": "organizer"
            },
            {
                "full_name": "Carlos Participante",
                "email": "carlos@eventcorp.com",
                "password": "password123",
                "role": "participant"
            }
        ]
        
        created_users = []
        
        for user in users:
            try:
                response = requests.post(
                    f"{self.base_url}/auth/register",
                    json=user,
                    headers={"Content-Type": "application/json"}
                )
                
                if response.status_code == 201:
                    print(f"✅ Usuario creado: {user['full_name']} ({user['role']})")
                    created_users.append(user)
                else:
                    print(f"❌ Error creando usuario {user['full_name']}: {response.text}")
                    
            except requests.exceptions.RequestException as e:
                print(f"❌ Error de conexión: {e}")
        
        return created_users
    
    def create_sample_content(self, organizer_token):
        """Crear contenido de muestra para la demostración"""
        self.print_header("Creación de Contenido de Muestra")
        
        # Headers con token de autenticación
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {organizer_token}"
        }
        
        # Crear publicación de muestra
        post_data = {
            "title": "Bienvenidos al Evento Corporativo 2025",
            "content": "Estamos emocionados de darles la bienvenida a nuestro evento anual. Tendremos charlas inspiradoras, networking y muchas sorpresas.",
            "image_url": "https://images.unsplash.com/photo-1540575467063-178a50c2df87?w=800",
            "tags": ["evento", "corporativo", "networking"]
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/posts/",
                json=post_data,
                headers=headers
            )
            
            if response.status_code == 201:
                print("✅ Publicación de muestra creada")
                post_id = response.json()["data"]["id"]
            else:
                print(f"❌ Error creando publicación: {response.text}")
                return None
                
        except requests.exceptions.RequestException as e:
            print(f"❌ Error de conexión: {e}")
            return None
        
        # Crear historia temporal
        story_data = {
            "content": "¡Recordatorio! El evento comienza en 2 horas. ¡No se lo pierdan!",
            "image_url": "https://images.unsplash.com/photo-1511795409834-ef04bbd61622?w=800"
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/stories/",
                json=story_data,
                headers=headers
            )
            
            if response.status_code == 201:
                print("✅ Historia temporal creada")
            else:
                print(f"❌ Error creando historia: {response.text}")
                
        except requests.exceptions.RequestException as e:
            print(f"❌ Error de conexión: {e}")
        
        return post_id
    
    def login_user(self, email, password):
        """Iniciar sesión con un usuario"""
        try:
            response = requests.post(
                f"{self.base_url}/auth/login",
                json={"email": email, "password": password},
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                data = response.json()["data"]
                return data["access_token"]
            else:
                print(f"❌ Error de login: {response.text}")
                return None
                
        except requests.exceptions.RequestException as e:
            print(f"❌ Error de conexión: {e}")
            return None
    
    def run_demo_checks(self):
        """Ejecutar verificaciones de la demostración"""
        self.print_header("Verificaciones de la Demostración")
        
        # Verificar endpoints principales
        endpoints = [
            ("/auth/register", "POST"),
            ("/auth/login", "POST"),
            ("/posts/", "GET"),
            ("/stories/", "GET"),
            ("/users/me", "GET")
        ]
        
        for endpoint, method in endpoints:
            try:
                if method == "GET":
                    response = requests.get(f"{self.base_url}{endpoint}")
                else:
                    response = requests.post(f"{self.base_url}{endpoint}")
                
                if response.status_code in [200, 201, 401, 403]:  # Respuestas válidas
                    print(f"✅ {method} {endpoint}: OK")
                else:
                    print(f"❌ {method} {endpoint}: Error {response.status_code}")
                    
            except requests.exceptions.RequestException as e:
                print(f"❌ {method} {endpoint}: Error de conexión")
    
    def print_demo_instructions(self):
        """Imprimir instrucciones para la demostración manual"""
        self.print_header("Instrucciones para la Demostración")
        
        instructions = [
            "1. Abrir navegador en: http://localhost:3000",
            "2. Registrar usuario organizador: ana@eventcorp.com / password123",
            "3. Registrar usuario participante: carlos@eventcorp.com / password123",
            "4. Como organizador, crear publicaciones e historias",
            "5. Como participante, interactuar con el contenido",
            "6. Probar funcionalidades: likes, comentarios, búsqueda",
            "7. Verificar historias temporales y notificaciones"
        ]
        
        for instruction in instructions:
            print(f"📋 {instruction}")
        
        print(f"\n🔗 URLs importantes:")
        print(f"   Frontend: {self.frontend_url}")
        print(f"   Backend API: {self.base_url}")
        print(f"   Documentación API: {self.base_url.replace('/api/v1', '')}/docs")
    
    def run_full_demo(self):
        """Ejecutar demostración completa"""
        self.print_header("Iniciando Demostración EventCorp")
        
        # Verificar servicios
        if not self.check_services():
            print("❌ Los servicios no están disponibles. Ejecuta 'docker-compose up -d' primero.")
            return False
        
        # Crear usuarios de prueba
        users = self.create_test_users()
        
        if not users:
            print("❌ No se pudieron crear usuarios de prueba")
            return False
        
        # Login como organizador
        organizer_token = self.login_user("ana@eventcorp.com", "password123")
        if organizer_token:
            # Crear contenido de muestra
            self.create_sample_content(organizer_token)
        
        # Ejecutar verificaciones
        self.run_demo_checks()
        
        # Mostrar instrucciones
        self.print_demo_instructions()
        
        print("\n🎉 ¡Demostración preparada exitosamente!")
        return True

def main():
    """Función principal"""
    print("🚀 EventCorp - Script de Demostración")
    print("=" * 50)
    
    demo = EventCorpDemo()
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "check":
            demo.check_services()
        elif command == "users":
            demo.create_test_users()
        elif command == "content":
            token = demo.login_user("ana@eventcorp.com", "password123")
            if token:
                demo.create_sample_content(token)
        elif command == "verify":
            demo.run_demo_checks()
        else:
            print("Comandos disponibles:")
            print("  python demo_script.py check    - Verificar servicios")
            print("  python demo_script.py users    - Crear usuarios de prueba")
            print("  python demo_script.py content  - Crear contenido de muestra")
            print("  python demo_script.py verify   - Verificar endpoints")
            print("  python demo_script.py          - Ejecutar demo completa")
    else:
        demo.run_full_demo()

if __name__ == "__main__":
    main() 