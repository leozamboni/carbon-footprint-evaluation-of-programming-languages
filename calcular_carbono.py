#!/usr/bin/env python3
"""Reproduce language carbon footprints from Pereira et al. 2021 energy norms."""
from __future__ import annotations
import csv, json
from pathlib import Path

BASE_J = 57.86  # C absolute energy (J), Pereira et al. 2021
EFS = {"global": 473.0, "brazil": 103.0, "eu": 213.0, "us": 384.0}  # gCO2e/kWh (Ember 2024)

LANGS = [
    ("C", "compiled", 1.00), ("Rust", "compiled", 1.03), ("C++", "compiled", 1.34),
    ("Ada", "compiled", 1.70), ("Java", "VM", 1.98), ("Pascal", "compiled", 2.14),
    ("Chapel", "compiled", 2.18), ("Lisp", "VM", 2.27), ("Ocaml", "compiled", 2.40),
    ("Fortran", "compiled", 2.52), ("Swift", "compiled", 2.79), ("Haskell", "compiled", 3.10),
    ("C#", "VM", 3.14), ("Go", "compiled", 3.23), ("Dart", "interpreted", 3.83),
    ("F#", "VM", 4.13), ("JavaScript", "interpreted", 4.45), ("Racket", "VM", 7.91),
    ("TypeScript", "interpreted", 21.50), ("Hack", "interpreted", 24.02),
    ("PHP", "interpreted", 29.30), ("Erlang", "VM", 42.23), ("Lua", "interpreted", 45.98),
    ("Jruby", "interpreted", 46.54), ("Ruby", "interpreted", 69.91),
    ("Python", "interpreted", 75.88), ("Perl", "interpreted", 79.58),
]

def main() -> None:
    rows = []
    for i, (lang, kind, norm) in enumerate(LANGS, 1):
        e_j = BASE_J * norm
        e_kwh = e_j / 3.6e6
        row = {"rank_energy": i, "language": lang, "execution_model": kind,
               "energy_norm": norm, "energy_j": e_j, "energy_kwh": e_kwh}
        for name, ef in EFS.items():
            row[f"co2_g_{name}"] = e_kwh * ef
        rows.append(row)
    out = Path(__file__).resolve().parent
    with open(out / "carbon_by_language.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader(); w.writerows(rows)
    with open(out / "carbon_by_language.json", "w") as f:
        json.dump({"base_energy_j_C": BASE_J, "emission_factors_g_per_kwh": EFS,
                   "source_energy": "Pereira et al. 2021 Table 4",
                   "source_ef": "Ember Global Electricity Review (2024 generation intensity)",
                   "rows": rows}, f, indent=2)
    print(f"Wrote {len(rows)} languages to {out}")

if __name__ == "__main__":
    main()
