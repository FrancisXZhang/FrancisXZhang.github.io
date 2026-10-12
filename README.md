# HomePage

The English website is `index.html`; the Chinese version is `index-zh.html`.
Publication entries remain in English on both pages.

After changing the English website, update the corresponding translations in
`scripts/build_zh.py` and regenerate the Chinese page:

```sh
python3 scripts/build_zh.py
```

The CV is generated separately with `python3 scripts/build_cv.py` (requires ReportLab).
