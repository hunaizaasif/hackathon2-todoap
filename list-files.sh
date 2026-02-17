#!/bin/bash

# Create a simple file listing for manual upload reference

echo "=== Phase 2 Files for Upload ==="
echo ""
echo "Root Directory Files:"
cd /mnt/e/Hackathon-2/phase-2
for file in Dockerfile main.py pyproject.toml uv.lock alembic.ini README_HF.md; do
    if [ -f "$file" ]; then
        size=$(ls -lh "$file" | awk '{print $5}')
        echo "  ✓ $file ($size)"
    fi
done

echo ""
echo "src/ Directory Structure:"
find src -type f -name "*.py" | sort | while read file; do
    size=$(ls -lh "$file" | awk '{print $5}')
    echo "  ✓ $file ($size)"
done

echo ""
echo "alembic/ Directory Structure:"
find alembic -type f \( -name "*.py" -o -name "*.mako" -o -name "README" \) | sort | while read file; do
    size=$(ls -lh "$file" | awk '{print $5}')
    echo "  ✓ $file ($size)"
done

echo ""
echo "Total files to upload: $(find . -type f \( -name "Dockerfile" -o -name "*.py" -o -name "*.toml" -o -name "*.lock" -o -name "*.ini" -o -name "*.md" -o -name "*.mako" -o -name "README" \) | wc -l)"
