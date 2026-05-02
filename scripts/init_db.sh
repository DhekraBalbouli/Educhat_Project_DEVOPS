#!/bin/sh

set -e

DB_FILE="/data/db.sqlite3"
CORPUS_DST="/data/corpus"

echo "=== Init volume EduChat ==="

if [ ! -d "$CORPUS_DST" ]; then
    echo "→ Copie du corpus YAML vers le volume..."
    cp -r /data/corpus "$CORPUS_DST"
    echo "✅ Corpus copié"
else
    echo "ℹ️  Corpus déjà présent — skipped"
fi

if [ ! -f "$DB_FILE" ]; then
    echo "→ Création de la base SQLite vide..."
    sqlite3 "$DB_FILE" "PRAGMA journal_mode=WAL;"
    echo "✅ Base SQLite initialisée : $DB_FILE"
else
    echo "ℹ️  Base SQLite déjà présente — skipped"
fi

echo "=== Init terminée ==="