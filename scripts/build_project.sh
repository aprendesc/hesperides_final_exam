#!/bin/bash
# build_project.sh - Construye el wheel del proyecto
#
# Uso: ./build_project.sh
#
# Este script es obligatorio en todo proyecto. Construye el wheel del proyecto
# y lo deposita en dist/

cd "$(dirname "$0")/.."

echo "=== Building Hesperides Final Exam ==="
echo ""

# Limpiar builds anteriores
echo "Cleaning previous builds..."
rm -rf build/ dist/ *.egg-info/

# Construir el wheel con uv
echo "Building wheel..."
uv build

if [ $? -eq 0 ]; then
    echo ""
    echo "✓ Build completed successfully!"
    echo "Wheel location: $(pwd)/dist/"
    ls -lh dist/
else
    echo ""
    echo "✗ Build failed!"
    exit 1
fi

