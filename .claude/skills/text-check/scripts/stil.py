#!/usr/bin/env python3
"""Stil-Analyse für deutsche Texte: zeigt Wiederholungen, Floskeln und
gleichförmigen Satzbau. Ändert den Text NICHT, gibt nur Hinweise.

Aufruf:  python3 stil.py DATEI    (oder - für stdin)
"""
import re
import statistics
import sys
from collections import Counter

FLOSKELN = [
    "darüber hinaus", "zusammenfassend lässt sich sagen", "abschließend lässt sich",
    "eine entscheidende rolle", "eine wichtige rolle",
    "eine zentrale rolle", "in der heutigen zeit", "in der heutigen welt",
    "es ist wichtig zu beachten", "es ist anzumerken", "nicht zuletzt",
    "im folgenden", "insgesamt lässt sich", "von großer bedeutung",
    "vielschichtig", "facettenreich", "maßgeblich", "essenziell",
    "ein tieferes verständnis", "es lässt sich festhalten", "letztendlich",
    "sowohl als auch", "nicht nur", "in diesem zusammenhang",
]

STOPP = set("""der die das und oder aber ein eine einer eines einem einen ist sind
war waren wird werden zu zur zum im in am an auf aus bei mit von vor nach für über
unter durch als auch nicht es sie er wir ich ihr man sich so wie dass da den dem des
noch nur schon sehr mehr kann können hat haben wurde wurden dieser diese dieses""".split())


def saetze(text):
    teile = re.split(r"(?<=[.!?])\s+", text.strip())
    return [s for s in teile if len(s.split()) >= 2]


def main():
    pfad = sys.argv[1] if len(sys.argv) > 1 else "-"
    text = sys.stdin.read() if pfad == "-" else open(pfad, encoding="utf-8").read()
    s = saetze(text)
    if not s:
        print("Kein Text gefunden.")
        return

    laengen = [len(x.split()) for x in s]
    print(f"Sätze: {len(s)}, Wörter: {sum(laengen)}")
    print(f"Satzlänge: Ø {statistics.mean(laengen):.1f} Wörter, "
          f"min {min(laengen)}, max {max(laengen)}", end="")
    if len(laengen) > 2:
        sd = statistics.pstdev(laengen)
        print(f", Streuung {sd:.1f}")
        if sd < 4:
            print("  Hinweis: Sätze sind sehr gleich lang -> wirkt eintönig. "
                  "Kurze und lange Sätze mischen.")
    else:
        print()

    lange = [(i + 1, n) for i, n in enumerate(laengen) if n > 30]
    if lange:
        print("Sehr lange Sätze (>30 Wörter): " +
              ", ".join(f"Satz {i} ({n})" for i, n in lange))

    anfaenge = Counter(x.split()[0].strip("„\"'(").lower() for x in s)
    wdh = [(w, n) for w, n in anfaenge.most_common() if n >= 3]
    if wdh:
        print("Häufige Satzanfänge: " + ", ".join(f"„{w}“ {n}x" for w, n in wdh))

    klein = text.lower()
    gef = [(f, klein.count(f)) for f in FLOSKELN if f in klein]
    if gef:
        print("Floskeln / formelhafte Wendungen:")
        for f, n in sorted(gef, key=lambda t: -t[1]):
            print(f"  „{f}“ {n}x")

    woerter = [w for w in re.findall(r"[a-zäöüß]{5,}", klein) if w not in STOPP]
    haeufig = [(w, n) for w, n in Counter(woerter).most_common(10) if n >= 4]
    if haeufig:
        print("Oft wiederholte Wörter: " + ", ".join(f"{w} {n}x" for w, n in haeufig))


if __name__ == "__main__":
    main()
