# Frozono-Grafic

Presentaciones semanales de la Reunión de Indicadores, publicadas con GitHub Pages.

- Portal: https://d0ct0re.github.io/Frozono-Grafic/
- Cada semana: `https://d0ct0re.github.io/Frozono-Grafic/semanas/AAAA-SNN/`  (ej. `semanas/2026-S43/`)
- Ir a una diapositiva: agrega `#N` al final (ej. `semanas/2026-S43/#18`)

## Estructura
```
index.html            portal con todas las semanas (lee presentaciones.json)
presentaciones.json   lista de semanas (la actualiza el script)
visor/                visor compartido (flechas, índice G, pantalla completa F)
semanas/AAAA-SNN/     una carpeta por semana
  slides.json         orden de diapositivas; cuáles son interactivas o animadas
  img/  thumb/        diapositivas fijas exportadas del PowerPoint
  live/               gráficas HTML interactivas/animadas de esa semana
herramientas/         nueva_semana.py
archivo/              versiones viejas
```

## Agregar una semana
```
python herramientas/nueva_semana.py "Semana_44.pptx" --semana 2026-S44 \
  --titulo "Semana 44 – Reunión de Indicadores" --fecha 2026-11-02 \
  --interactiva 18=cargas.html --interactiva 22=aumento.html
```
También acepta una carpeta con las diapositivas exportadas como JPG desde PowerPoint.
`--animar 5=zoom` o `--animar 5=up` le pone animación de entrada a una diapositiva fija.

## slides.json
```json
{"titulo":"Semana 43 – Reunión de Indicadores","slides":[
  {"img":"img/01.jpg","thumb":"thumb/01.jpg"},
  {"img":"img/18.jpg","thumb":"thumb/18.jpg","live":"live/cargas-identificadas-s43.html"}
]}
```
La imagen de una diapositiva interactiva se muestra mientras carga la gráfica en vivo.
