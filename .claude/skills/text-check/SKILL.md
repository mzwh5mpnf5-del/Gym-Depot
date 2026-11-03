---
name: text-check
description: Prüft Texte auf zwei Arten - (1) findet und entfernt unsichtbare/ungewöhnliche Unicode-Zeichen (Zero-Width, geschützte Leerzeichen, Bidi-Steuerzeichen, Tag-Zeichen); (2) gibt Stil-Feedback zu Wortwahl und Satzbau (Floskeln, Wiederholungen, eintönige Satzlängen), damit der Nutzer seinen Text selbst verbessert. Verwenden bei "Text bereinigen", "Wasserzeichen entfernen", "versteckte Zeichen", "Stil prüfen", "klingt mein Text gut", "Feedback zu meinem Text".
---

# Text-Check

## Grundregeln (immer einhalten)
- Ehrlich bleiben: Nach aktuellem Kenntnisstand bauen Claude und ChatGPT keine
  Wasserzeichen aus unsichtbaren Zeichen ein. Statistische Wasserzeichen (z. B.
  Googles SynthID bei Gemini) lassen sich ohne den geheimen Schlüssel weder
  erkennen noch per Skript gezielt entfernen. Nichts anderes behaupten.
- Teil 2 ist **Feedback, kein Umschreiben**: Stellen markieren, erklären warum,
  höchstens ein kurzes Beispiel zeigen. Der Nutzer formuliert selbst um.
- Keine KI-generierten Texte so umschreiben, dass sie als selbst geschrieben
  durchgehen oder KI-Detektoren umgehen. Wenn danach gefragt wird: freundlich
  ablehnen und Feedback zum eigenen Text anbieten.

## Teil 1: Unsichtbare Zeichen
1. Text in eine Datei im Scratchpad schreiben (oder vorhandene Datei nutzen).
2. Prüfen: `python3 <skill-ordner>/scripts/clean.py DATEI --report`
3. Bereinigen: `python3 <skill-ordner>/scripts/clean.py DATEI -o DATEI_sauber.txt`
   Optional `--typografie` (ersetzt „“ ’ – — … durch ASCII; im Deutschen sind „“ korrekt,
   also nur auf Wunsch).
4. Bericht zeigen und den bereinigten Text ausgeben.

Entfernt: U+200B/C/D, U+2060, U+FEFF, U+00AD, Bidi-Zeichen (U+200E/F, U+202A–202E,
U+2066–2069), Tag-Zeichen (U+E0000–E007F), sonstige Format-Zeichen (Cf).
Ersetzt durch Leerzeichen: U+00A0, U+202F, U+2000–200A, U+205F, U+3000.
Behält: Emoji-Joiner in Emojis, Variation Selectors, Flaggen-Tags.

## Teil 2: Stil-Feedback
1. `python3 <skill-ordner>/scripts/stil.py DATEI` ausführen. Liefert Satzlängen und
   Streuung, sehr lange Sätze, häufige Satzanfänge, Floskeln, oft wiederholte Wörter.
2. Ergebnis zusammen mit eigenem Lesen auswerten und als Liste zurückgeben:
   - konkrete Stelle (Zitat) → was auffällt → Tipp, worauf achten
   - z. B. "3 Sätze beginnen mit ‚Darüber hinaus‘ → Übergänge abwechseln oder weglassen"
3. Auf Inhalt achten, nicht nur Form: Wo fehlen eigene Beispiele, eigene Meinung,
   Belege/Quellen? Das macht einen Text am meisten zu "deinem".
4. Den Text nicht komplett neu schreiben.
