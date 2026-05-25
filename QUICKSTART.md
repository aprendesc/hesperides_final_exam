# Guía Rápida - Hesperides Final Exam

## Instalación

```bash
# Navegar al directorio del proyecto
cd /Users/alejandroprendes/Desktop/projects/code

# Instalar dependencias base
uv sync

# (Opcional) Instalar con dependencias para servidor
uv sync --extra server
```

## Ejecutar la Aplicación

### Modo 1: Script principal (recomendado para desarrollo)

```bash
# Ejecutar main.py directamente
python code/apps/main/main.py
```

**Ventaja:** Usa configuración por defecto hardcodeada. Ideal para depuración rápida.

### Modo 2: CLI interactiva

```bash
# Ejecutar como módulo Python
python -m code.apps.main

# O si está instalado:
hesperides-main
```

**Ventaja:** Menú interactivo para seleccionar modo y configuración.

### Modo 3: Servidor HTTP

```bash
# Instalar primero las dependencias de servidor
uv sync --extra server

# Iniciar el servidor
python code/apps/main/server.py
```

**Endpoints disponibles:**
- `GET /health` — estado de la aplicación
- `POST /run` — ejecutar con parámetros personalizados
- `GET /config` — ver configuración actual

**Ejemplo de request:**
```bash
curl -X POST http://localhost:8000/run \
  -H "Content-Type: application/json" \
  -d '{"mode": "production"}'
```

### Modo 4: Script de construcción

```bash
# Construir el wheel del proyecto
./scripts/build_project.sh
```

## Ejecutar Tests

```bash
# Tests funcionales
python tests/functional_tests/test_main_app.py

# O con pytest
uv run pytest tests/functional_tests/ -v

# Tests unitarios
uv run pytest tests/unit/ -v

# Tests de integración
uv run pytest tests/integration/ -v
```

## Ejecutar Experiments (Etapa 1)

```bash
python experiments/framework_exploration_v1.py
```

## Estructura Clave

| Carpeta | Propósito |
|---------|-----------|
| `hesperides_final_exam/apps/main/` | Aplicación principal con Main, CLI, Server |
| `hesperides_final_exam/modules/` | Módulos reutilizables por dominio |
| `experiments/` | Scripts de exploración (Etapa 1) |
| `tests/` | Tests unitarios, integración, funcionales |
| `docs/` | Documentación y diseño |
| `data/` | Datasets (excluidos de git) |
| `models/` | Artefactos entrenados (excluidos de git) |

## Configuración

### Variables de Entorno

Copiar `.env.example` a `.env` y rellenar:

```bash
cp .env .env
```

Editar `.env` con valores reales. **Nunca commitear** `.env` con credentials.

### YAML de Configuración

Ubicado en `hesperides_final_exam/apps/main/configs/default.yaml`

Editar para cambiar comportamiento por defecto:

```yaml
application:
  name: "code"
  mode: "development"  # development | production | custom
```

## Próximas Acciones

1. **Definir dominios:** Identificar los dominios funcionales del proyecto
2. **Crear módulos:** Implementar módulos en `hesperides_final_exam/modules/`
3. **Escribir experiments:** Explorat nuevas ideas en `experiments/`
4. **Expandir tests:** Añadir cobertura en `tests/`
5. **Documentar:** Actualizar `docs/ARCHITECTURE.md`

## Referencias

- **Patrón de diseño:** Personal Design Pattern (en la raíz del proyecto)
- **Etapas:** Experiment (v1) → Modular PoC (v2)
- **Documentación:** `docs/ARCHITECTURE.md`

---

**Versión:** 0.1.0 | **Última actualización:** 2026-05-22

