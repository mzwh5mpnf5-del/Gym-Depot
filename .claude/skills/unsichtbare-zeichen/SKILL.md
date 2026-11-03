---
name: unsichtbare-zeichen
description: Findet und entfernt unsichtbare oder ungewöhnliche Unicode-Zeichen in Text (Zero-Width-Zeichen, geschützte Leerzeichen, Bidi-Steuerzeichen, Soft Hyphens, Unicode-Tag-Zeichen). Verwenden, wenn der Nutzer einen Text "bereinigen", auf versteckte Zeichen prüfen oder ein "Wasserzeichen entfernen" möchte.
---

# Unsichtbare Zeichen entfernen

## Wichtig, ehrlich kommunizieren
- Nach aktuellem Kenntnisstand bauen Claude und ChatGPT **keine** absichtlichen
  Wasserzeichen aus unsichtbaren Zeichen in ihre Antworten ein. Gefundene Zeichen
  stammen meist von Copy-Paste, Word, PDFs oder Webseiten.
- Das Entfernen ändert nichts daran, ob ein Text von KI-Detektoren oder Lehrkräften
  als KI-Text erkannt wird. Das nicht versprechen.

## Ablauf
1. Text in eine Datei im Scratchpad schreiben (oder vorhandene Datei nutzen).
2. Erst prüfen:
   `python3 .claude/skills/unsichtbare-zeichen/scripts/clean.py DATEI --report`
3. Dann bereinigen:
   `python3 .claude/skills/unsichtbare-zeichen/scripts/clean.py DATEI -o DATEI_sauber.txt`
   Optional `--typografie`, um „“ ’ – — … durch einfache ASCII-Zeichen zu ersetzen
   (nur wenn der Nutzer das will, im Deutschen sind „“ korrekt).
4. Dem Nutzer den Bericht zeigen (welche Zeichen, wie oft) und den bereinigten Text geben.

## Was das Skript macht
- **Entfernt:** U+200B/C/D, U+2060, U+FEFF, U+00AD, Bidi-Steuerzeichen
  (U+200E/F, U+202A–202E, U+2066–2069), Unicode-Tag-Zeichen (U+E0000–E007F),
  weitere unsichtbare Format-Zeichen (Kategorie Cf).
- **Ersetzt durch normales Leerzeichen:** U+00A0, U+202F, U+2000–200A, U+205F, U+3000.
- **Behält:** Emoji-Joiner in Emoji-Sequenzen, Variation Selectors (U+FE00–FE0F),
  Tag-Zeichen in Flaggen-Emojis.
