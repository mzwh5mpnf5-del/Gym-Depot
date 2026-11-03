#!/usr/bin/env python3
"""Findet und entfernt unsichtbare / ungewöhnliche Unicode-Zeichen in Text.

Aufruf:
  python3 clean.py DATEI            -> bereinigt, schreibt nach stdout
  python3 clean.py DATEI -o AUS     -> bereinigt, schreibt in Datei AUS
  python3 clean.py DATEI --report   -> nur Bericht, nichts ändern
  python3 clean.py - < text.txt     -> liest von stdin
Optionen:
  --typografie   ersetzt zusätzlich „“ ” ‘ ’ – — … durch einfache Zeichen
"""
import argparse
import sys
import unicodedata
from collections import Counter

# Zeichen, die komplett entfernt werden
ENTFERNEN = {
    0x200B: "Zero Width Space",
    0x200C: "Zero Width Non-Joiner",
    0x200D: "Zero Width Joiner",
    0x2060: "Word Joiner",
    0xFEFF: "Zero Width No-Break Space / BOM",
    0x00AD: "Soft Hyphen (weiches Trennzeichen)",
    0x180E: "Mongolian Vowel Separator",
    0x200E: "Left-to-Right Mark",
    0x200F: "Right-to-Left Mark",
    0x061C: "Arabic Letter Mark",
    **{c: "Bidi-Steuerzeichen" for c in range(0x202A, 0x202F)},
    **{c: "Bidi-Isolat" for c in range(0x2066, 0x206A)},
    **{c: "Unsichtbarer Operator" for c in range(0x2061, 0x2065)},
}

# Zeichen, die durch ein normales Leerzeichen ersetzt werden
ZU_LEERZEICHEN = {
    0x00A0: "No-Break Space (geschütztes Leerzeichen)",
    0x202F: "Narrow No-Break Space",
    0x205F: "Medium Mathematical Space",
    0x3000: "Ideographic Space",
    **{c: "Typografisches Leerzeichen" for c in range(0x2000, 0x200B)},
}

TYPOGRAFIE = {
    "“": '"', "”": '"', "„": '"', "«": '"', "»": '"',
    "‘": "'", "’": "'", "‚": "'",
    "–": "-", "—": "-", "…": "...",
}


def ist_tag_zeichen(cp: int) -> bool:
    # Unicode-Tag-Zeichen (U+E0000–U+E007F), unsichtbar, können Text verstecken.
    # Ausnahme: Teil einer Flaggen-Emoji-Sequenz (nach U+1F3F4).
    return 0xE0000 <= cp <= 0xE007F


def bereinigen(text: str, typografie: bool):
    funde = Counter()
    raus = []
    for i, ch in enumerate(text):
        cp = ord(ch)
        if cp in ENTFERNEN:
            # ZWJ in Emoji-Sequenzen behalten (z. B. Familien-Emojis)
            if cp == 0x200D and i > 0 and i + 1 < len(text) \
                    and ord(text[i - 1]) > 0xFFFF and ord(text[i + 1]) > 0x2000:
                raus.append(ch)
                continue
            funde[(cp, ENTFERNEN[cp], "entfernt")] += 1
            continue
        if ist_tag_zeichen(cp):
            vorher = "".join(raus)
            if "\U0001F3F4" in vorher[-12:]:
                raus.append(ch)
                continue
            funde[(cp, "Unicode-Tag-Zeichen (versteckter Text)", "entfernt")] += 1
            continue
        if cp in ZU_LEERZEICHEN:
            funde[(cp, ZU_LEERZEICHEN[cp], "-> Leerzeichen")] += 1
            raus.append(" ")
            continue
        if typografie and ch in TYPOGRAFIE:
            funde[(cp, unicodedata.name(ch, "?"), f"-> {TYPOGRAFIE[ch]}")] += 1
            raus.append(TYPOGRAFIE[ch])
            continue
        # Sonstige unsichtbare Format-Zeichen (Kategorie Cf) melden und entfernen
        if unicodedata.category(ch) == "Cf" and not (0xFE00 <= cp <= 0xFE0F):
            funde[(cp, unicodedata.name(ch, "Format-Zeichen"), "entfernt")] += 1
            continue
        raus.append(ch)
    return "".join(raus), funde


def bericht(funde: Counter) -> str:
    if not funde:
        return "Keine unsichtbaren oder ungewöhnlichen Zeichen gefunden."
    zeilen = ["Gefundene Zeichen:"]
    for (cp, name, aktion), n in sorted(funde.items()):
        zeilen.append(f"  U+{cp:04X}  {name}: {n}x ({aktion})")
    zeilen.append(f"Gesamt: {sum(funde.values())}")
    return "\n".join(zeilen)


def main():
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("datei", help="Eingabedatei oder - für stdin")
    p.add_argument("-o", "--ausgabe", help="Ausgabedatei (sonst stdout)")
    p.add_argument("--report", action="store_true", help="nur Bericht")
    p.add_argument("--typografie", action="store_true",
                   help="typografische Anführungszeichen/Striche vereinfachen")
    a = p.parse_args()

    text = sys.stdin.read() if a.datei == "-" else open(a.datei, encoding="utf-8").read()
    sauber, funde = bereinigen(text, a.typografie)
    print(bericht(funde), file=sys.stderr)
    if a.report:
        return
    if a.ausgabe:
        with open(a.ausgabe, "w", encoding="utf-8") as f:
            f.write(sauber)
        print(f"Gespeichert: {a.ausgabe}", file=sys.stderr)
    else:
        sys.stdout.write(sauber)


if __name__ == "__main__":
    main()
