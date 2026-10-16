# -*- coding: utf-8 -*-
"""Сборка эмулятора приложения «Лёд MosDomIce»: подставляет фото из приложения."""
import base64
import datetime
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))          # ...\MosDomIce\GPT
ASSETS = os.path.join(ROOT, "ice-app", "Sources", "Resources", "Assets.xcassets")
PHOTOS = ["lump", "frappe", "flake", "cups", "cube5", "stick", "glass-craft", "glass-darts", "dry"]


def data_uri(name, ext="jpg"):
    mime = "image/png" if ext == "png" else "image/jpeg"
    path = os.path.join(ASSETS, name + ".imageset", name + "." + ext)
    with open(path, "rb") as f:
        return "data:" + mime + ";base64," + base64.b64encode(f.read()).decode()


def main():
    with open(os.path.join(HERE, "template.html"), encoding="utf-8") as f:
        html = f.read()
    images = "{" + ",".join('"%s":"%s"' % (n, data_uri(n)) for n in PHOTOS) + "}"
    stamp = datetime.datetime.now().strftime("%d.%m.%Y %H:%M")
    logo = data_uri("logomark", "png")
    html = (html.replace("__IMG__", images)
                .replace("__LOGO__", logo)
                .replace("__LOGO_HEADER__", logo)
                .replace("__THEME_NAME__", "a")
                .replace("__VERSION__", stamp))
    with open(os.path.join(HERE, "index.html"), "w", encoding="utf-8", newline="\n") as f:
        f.write(html)
    print("эмулятор собран:", os.path.join(HERE, "index.html"))


if __name__ == "__main__":
    main()
