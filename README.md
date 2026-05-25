# Hesperides Final Exam

Framework de ingeniería de software personal para proyectos de aprendizaje y exploración.

## Inicio rápido

### Prerequisitos

- Python ≥ 3.11
- `uv` (gestor de paquetes ultrarrápido)

### Instalación

```bash
# Clonar o navegar al repositorio
cd code

# Instalar dependencias
uv sync

# Ejecutar la aplicación por defecto
uv run python -m code.apps.main.main
```

## Estructura

```
hesperides_final_exam/
├── data/              # Datasets y datos persistidos
├── docs/              # Documentación de diseño
├── models/            # Artefactos entrenados
├── scripts/           # Entry points ejecutables
├── experiments/       # Scripts de exploración (Etapa 1)
├── tests/             # Tests (unit, integration, functional)
├── hesperides_final_exam/  # Paquete principal
│   ├── apps/          # Aplicaciones desplegables
│   └── modules/       # Librería reutilizable
├── pyproject.toml     # Configuración del proyecto
└── README.md          # Este archivo
```

## Desarrollo

Seguir las guidelines de [personal_design_pattern.md](./docs/design_pattern.md).

### Etapas de desarrollo

1. **Experiment (Etapa 1):** Scripts monolíticos en `experiments/`
2. **Modular PoC (Etapa 2):** Módulos estructurados en `hesperides_final_exam/`

## Testing

```bash
# Ejecutar tests unitarios
uv run pytest tests/unit

# Ejecutar tests de integración
uv run pytest tests/integration

# Ejecutar tests funcionales
uv run pytest tests/functional_tests
```

## Licencia

Interno - Proyectos de aprendizaje personal.

