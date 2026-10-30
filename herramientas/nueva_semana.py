#!/usr/bin/env python3
"""Agrega una presentación semanal al sitio.

Uso:
  python herramientas/nueva_semana.py PRESENTACION.pptx --semana 2026-S44 \
      --titulo "Semana 44 – Reunión de Indicadores" --fecha 2026-11-02 \
      --interactiva 18=cargas.html --interactiva 22=aumento.html

  PRESENTACION puede ser un .pptx/.pdf o una carpeta con las diapositivas exportadas
  como imagen (en PowerPoint: Archivo > Exportar > JPEG, "Todas las diapositivas").
  Los .html de --interactiva se buscan en --live-dir (por defecto, junto a la presentación)
  y se copian a semanas/<semana>/live/.
Requiere: Pillow. Para .pptx: LibreOffice (soffice) y pdftoppm (poppler).
"""
import argparse, json, os, re, shutil, subprocess, sys, tempfile, glob
from PIL import Image

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def a_imagenes(origen, tmp):
    if os.path.isdir(origen):
        fs = [f for f in os.listdir(origen) if f.lower().endswith((".jpg", ".jpeg", ".png"))]
        num = lambda f: int((re.findall(r"\d+", f) or ["0"])[-1])
        return [os.path.join(origen, f) for f in sorted(fs, key=num)]
    pdf = origen
    if origen.lower().endswith((".pptx", ".ppt")):
        subprocess.run(["soffice", "--headless", "--convert-to", "pdf", "--outdir", tmp, origen], check=True, capture_output=True)
        pdf = os.path.join(tmp, os.path.splitext(os.path.basename(origen))[0] + ".pdf")
    subprocess.run(["pdftoppm", "-r", "144", "-png", pdf, os.path.join(tmp, "p")], check=True)
    return sorted(glob.glob(os.path.join(tmp, "p-*.png")))

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("origen"); ap.add_argument("--semana", required=True, help="ej. 2026-S44")
    ap.add_argument("--titulo", required=True); ap.add_argument("--fecha", default="")
    ap.add_argument("--interactiva", action="append", default=[], help="N=archivo.html")
    ap.add_argument("--animar", action="append", default=[], help="N=zoom|up  (animación de entrada para una diapositiva fija)")
    ap.add_argument("--live-dir", default=None)
    a = ap.parse_args()
    dest = os.path.join(RAIZ, "semanas", a.semana)
    for sub in ("img", "thumb", "live"): os.makedirs(os.path.join(dest, sub), exist_ok=True)
    live = dict(x.split("=", 1) for x in a.interactiva); anim = dict(x.split("=", 1) for x in a.animar)
    live_dir = a.live_dir or (a.origen if os.path.isdir(a.origen) else os.path.dirname(os.path.abspath(a.origen)))
    with tempfile.TemporaryDirectory() as tmp:
        imgs = a_imagenes(a.origen, tmp); slides = []
        for i, f in enumerate(imgs, 1):
            im = Image.open(f).convert("RGB")
            if im.width > 1920: im = im.resize((1920, round(im.height * 1920 / im.width)), Image.LANCZOS)
            im.save(os.path.join(dest, "img", f"{i:02d}.jpg"), quality=86, optimize=True, progressive=True)
            th = im.copy(); th.thumbnail((480, 270)); th.save(os.path.join(dest, "thumb", f"{i:02d}.jpg"), quality=80)
            s = {"img": f"img/{i:02d}.jpg", "thumb": f"thumb/{i:02d}.jpg"}
            if str(i) in live:
                src = live[str(i)]; src_path = src if os.path.isabs(src) else os.path.join(live_dir, src)
                if os.path.exists(src_path): shutil.copy(src_path, os.path.join(dest, "live", os.path.basename(src)))
                elif not os.path.exists(os.path.join(dest, "live", os.path.basename(src))): sys.exit(f"No encuentro {src_path}")
                s["live"] = "live/" + os.path.basename(src)
            if str(i) in anim: s["anim"] = anim[str(i)]
            slides.append(s)
    json.dump({"titulo": a.titulo, "slides": slides}, open(os.path.join(dest, "slides.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    shutil.copy(os.path.join(RAIZ, "visor", "plantilla.html"), os.path.join(dest, "index.html"))
    man_p = os.path.join(RAIZ, "presentaciones.json")
    man = json.load(open(man_p, encoding="utf-8")) if os.path.exists(man_p) else {"presentaciones": []}
    man["presentaciones"] = [p for p in man["presentaciones"] if p["id"] != a.semana]
    man["presentaciones"].append({"id": a.semana, "titulo": a.titulo, "fecha": a.fecha, "diapositivas": len(slides),
                                  "interactivas": len(live), "portada": f"semanas/{a.semana}/thumb/01.jpg", "url": f"semanas/{a.semana}/"})
    man["presentaciones"].sort(key=lambda p: p["id"], reverse=True)
    json.dump(man, open(man_p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"Listo: semanas/{a.semana}/  ({len(slides)} diapositivas, {len(live)} interactivas)")

if __name__ == "__main__": main()
