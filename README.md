# Да ли ОН и даље прича?

Šala: jedna stranica koja kaže **ДА** ili **НЕ** — da li u Narodnoj skupštini upravo govori Aleksandar Vučić.

Strana je statična (GitHub Pages). Ko govori, čita sa [mikrofon.zailiprotiv.rs](https://mikrofon.zailiprotiv.rs)
(`stanje.js`), koji to čita iz potpisa ispod govornika u prenosu. Ukupno vreme po završenim danima je u
`ukupno.json`; pravi ga `tools/ukupno.py` u GitHub Actions (`.github/workflows/pages.yml`), na svaku promenu i na
sat. Današnji dan strana broji sama.

- `index.html`: cela strana (stil i skripta u njoj).
- `sw.js`: da klik na obaveštenje „Престао је да прича“ vrati na stranu.
- Proba lokalno: `python3 -m http.server` u ovom folderu (ukupno.json: `python3 tools/ukupno.py > ukupno.json`).
