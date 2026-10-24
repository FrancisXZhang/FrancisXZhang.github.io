# HomePage

The English website is `index.html`; the Chinese version is `index-zh.html`.
Publication titles, authors, venues, links, and topic tags remain in English on
both pages. Contribution notes are translated into Chinese on `index-zh.html`.

After changing the English website, update the corresponding translations in
`scripts/build_zh.py` (including `CONTRIBUTION_TRANSLATIONS` for contribution notes)
and regenerate the Chinese page:

```sh
python3 scripts/build_zh.py
```

The CV is generated separately with `python3 scripts/build_cv.py` (requires ReportLab).
