#!/bin/bash

# ===========================================
# EventCorp - Script de Demostración
# ===========================================

set -e  # Salir si hay algún error

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Función para imprimir mensajes
print_header() {
    echo -e "\n${BLUE}==========================================${NC}"
    echo -e "${BLUE}🎬 $1${NC}"
    echo -e "${BLUE}==========================================${NC}"
}

print_step() {
    echo -e "\n${YELLOW}📋 $1${NC}"
    echo -e "${YELLOW}------------------------------------------${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

# Verificar que Docker esté instalado
check_docker() {
    print_step "Verificando Docker"
    
    if ! command -v docker &> /dev/null; then
        print_error "Docker no está instalado"
        exit 1
    fi
    
    if ! command -v docker-compose &> /dev/null; then
        print_error "Docker Compose no está instalado"
        exit 1
    fi
    
    print_success "Docker y Docker Compose están instalados"
}

# Verificar que los puertos estén disponibles
check_ports() {
    print_step "Verificando puertos disponibles"
    
    if lsof -Pi :3000 -sTCP:LISTEN -t >/dev/null 2>&1; then
        print_error "Puerto 3000 ya está en uso"
        exit 1
    fi
    
    if lsof -Pi :8000 -sTCP:LISTEN -t >/dev/null 2>&1; then
        print_error "Puerto 8000 ya está en uso"
        exit 1
    fi
    
    print_success "Puertos 3000 y 8000 están disponibles"
}

# Iniciar servicios
start_services() {
    print_step "Iniciando servicios con Docker Compose"
    
    print_info "Construyendo y iniciando contenedores..."
    docker-compose up -d --build
    
    print_info "Esperando que los servicios estén listos..."
    sleep 10
    
    # Verificar que los servicios estén corriendo
    if docker-compose ps | grep -q "Up"; then
        print_success "Servicios iniciados correctamente"
    else
        print_error "Error al iniciar servicios"
        docker-compose logs
        exit 1
    fi
}

# Verificar servicios
check_services() {
    print_step "Verificando que los servicios estén funcionando"
    
    # Verificar backend
    if curl -s http://localhost:8000/api/v1/health > /dev/null 2>&1; then
        print_success "Backend API funcionando"
    else
        print_error "Backend API no responde"
        return 1
    fi
    
    # Verificar frontend
    if curl -s http://localhost:3000 > /dev/null 2>&1; then
        print_success "Frontend funcionando"
    else
        print_error "Frontend no responde"
        return 1
    fi
    
    return 0
}

# Ejecutar script de demostración
run_demo_script() {
    print_step "Ejecutando script de demostración"
    
    if [ -f "demo_script.py" ]; then
        print_info "Ejecutando script de Python..."
        python3 demo_script.py
    else
        print_error "Script demo_script.py no encontrado"
        return 1
    fi
}

# Mostrar información de acceso
show_access_info() {
    print_header "Información de Acceso"
    
    echo -e "${GREEN}🎯 URLs de Acceso:${NC}"
    echo -e "   Frontend: ${BLUE}http://localhost:3000${NC}"
    echo -e "   Backend API: ${BLUE}http://localhost:8000${NC}"
    echo -e "   Documentación API: ${BLUE}http://localhost:8000/docs${NC}"
    
    echo -e "\n${GREEN}👥 Usuarios de Prueba:${NC}"
    echo -e "   Organizador: ${BLUE}ana@eventcorp.com${NC} / ${BLUE}password123${NC}"
    echo -e "   Participante: ${BLUE}carlos@eventcorp.com${NC} / ${BLUE}password123${NC}"
    
    echo -e "\n${GREEN}📋 Comandos Útiles:${NC}"
    echo -e "   Ver logs: ${BLUE}docker-compose logs -f${NC}"
    echo -e "   Reiniciar: ${BLUE}docker-compose restart${NC}"
    echo -e "   Detener: ${BLUE}docker-compose down${NC}"
}

# Función principal
main() {
    print_header "EventCorp - Iniciando Demostración"
    
    # Verificar prerequisitos
    check_docker
    check_ports
    
    # Iniciar servicios
    start_services
    
    # Verificar servicios
    if check_services; then
        print_success "Todos los servicios están funcionando"
    else
        print_error "Algunos servicios no están funcionando"
        print_info "Revisando logs..."
        docker-compose logs --tail=20
        exit 1
    fi
    
    # Ejecutar script de demo
    if run_demo_script; then
        print_success "Script de demostración ejecutado"
    else
        print_error "Error ejecutando script de demostración"
    fi
    
    # Mostrar información de acceso
    show_access_info
    
    print_header "🎉 ¡Demostración Lista!"
    print_info "Abre http://localhost:3000 en tu navegador para comenzar"
}

# Función de limpieza
cleanup() {
    print_step "Limpiando recursos"
    
    print_info "Deteniendo contenedores..."
    docker-compose down
    
    print_success "Limpieza completada"
}

# Manejar argumentos de línea de comandos
case "${1:-}" in
    "start")
        main
        ;;
    "stop")
        cleanup
        ;;
    "restart")
        cleanup
        sleep 2
        main
        ;;
    "logs")
        docker-compose logs -f
        ;;
    "status")
        docker-compose ps
        ;;
    "help"|"-h"|"--help")
        echo -e "${BLUE}EventCorp - Script de Demostración${NC}"
        echo -e "\n${YELLOW}Uso:${NC}"
        echo -e "  $0 start    - Iniciar demostración completa"
        echo -e "  $0 stop     - Detener servicios"
        echo -e "  $0 restart  - Reiniciar servicios"
        echo -e "  $0 logs     - Ver logs en tiempo real"
        echo -e "  $0 status   - Ver estado de servicios"
        echo -e "  $0 help     - Mostrar esta ayuda"
        echo -e "\n${YELLOW}Ejemplo:${NC}"
        echo -e "  $0 start"
        ;;
    *)
        main
        ;;
esac 