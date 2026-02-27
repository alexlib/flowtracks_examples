#!/bin/bash
# Convert all .ipynb notebooks in jupyter_notebooks to marimo format in marimo_notebooks

SRC_DIR="jupyter_notebooks"
DEST_DIR="marimo_notebooks"

mkdir -p "$DEST_DIR"

for nb in "$SRC_DIR"/*.ipynb; do
    base=$(basename "$nb" .ipynb)
    marimo_out="$DEST_DIR/$base.py"
    marimo convert "$nb" -o "$marimo_out"
done

echo "Conversion complete. Marimo notebooks are in $DEST_DIR."
