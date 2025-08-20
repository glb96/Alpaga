#!/usr/bin/env bash
set -euo pipefail

# 1) Nettoyer/Préparer
rm -rf docs
mkdir -p docs

# 2) Construire la doc Sphinx depuis Wiki_raw vers docs/
# (tu peux utiliser 'make html' si tu as un Makefile)
python3.7 -m sphinx -b html Wiki_raw docs

# 3) Désactiver Jekyll pour GitHub Pages
touch docs/.nojekyll

