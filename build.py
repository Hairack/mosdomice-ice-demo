# -*- coding: utf-8 -*-
"""Сборка эмулятора приложения «Лёд MosDomIce»: подставляет фото из приложения."""
import base64
import datetime
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)                            # ...\MosDomIce\GPT
ASSETS = os.path.join(ROOT, "ice-app", "Sources", "Resources", "Assets.xcassets")
PHOTOS = ["lump", "frappe", "flake", "cups", "cube5", "stick", "glass-craft", "glass-darts", "dry"]

# Файл приложения для Android лежит рядом с сайтом.
APK_NAME = "ice-order-android.apk"


def data_uri(name, ext="jpg"):
    mime = "image/png" if ext == "png" else "image/jpeg"
    path = os.path.join(ASSETS, name + ".imageset", name + "." + ext)
    with open(path, "rb") as f:
        return "data:" + mime + ";base64," + base64.b64encode(f.read()).decode()


def calc_uri():
    """Иконка калькулятора: лежит в наборе calc.imageset под именем calc@3x.png."""
    path = os.path.join(ASSETS, "calc.imageset", "calc@3x.png")
    import base64
    with open(path, "rb") as f:
        return "data:image/png;base64," + base64.b64encode(f.read()).decode()


# Каналы отправки заявок. Заявка уходит по первому доступному: если площадка
# недоступна из России, приложение автоматически переходит к следующему.
ORDER_CHANNELS = [
    # Канал 1: приёмник на Google (доступен в России без VPN), шлёт заявку в Telegram.
    {"url": "https://script.google.com/macros/s/AKfycbyLZTm0jd3Z_LZ_VihIOyk32-YTaP48zUIabGazaAkg_djwZeLhM15VOz1XRQ_onsCzGg/exec",
     "secret": "mosdomice-ice-2026-relay-key"},
    # Канал 2: второй приёмник на Google — другая учётная запись и площадка.
    {"url": "https://script.google.com/macros/s/AKfycbyplUBROVn-A4g3avZRQd1ajmvANryuyiHWugrQOptUp11lXHEk86H1Fh90mJWbXy_S/exec",
     "secret": "mosdomice-ice-2026-relay-key"},
    # Канал 3: резервный приёмник на Cloudflare (доступен из России в сетях без фильтрации).
    {"url": "https://ice-relay.mosdombar.workers.dev/",
     "secret": "mosdomice-ice-2026-relay-key"},
    # Канал 4: прежний приёмник на нашем сервере (когда поднимется).
    {"url": "https://ledok.store/web-order.php", "secret": "1589c6b2986a630458c97bf44e3344a2f9367e0ba4a2b443"},
]

PHOTOS = ["lump", "frappe", "flake", "cups", "cube5", "stick", "glass-craft", "glass-darts", "dry"]

# Файл приложения для Android лежит рядом с сайтом.
APK_NAME = "ice-order-android.apk"


def data_uri(name, ext="jpg"):
    mime = "image/png" if ext == "png" else "image/jpeg"
    path = os.path.join(ASSETS, name + ".imageset", name + "." + ext)
    with open(path, "rb") as f:
        return "data:" + mime + ";base64," + base64.b64encode(f.read()).decode()


def calc_uri():
    """Иконка калькулятора: лежит в наборе calc.imageset под именем calc@3x.png."""
    path = os.path.join(ASSETS, "calc.imageset", "calc@3x.png")
    import base64
    with open(path, "rb") as f:
        return "data:image/png;base64," + base64.b64encode(f.read()).decode()



WORK = os.path.join(ROOT, "work")


def cocktail_images():
    """102 фото коктейлей (облегчённые) как data-URI."""
    import json
    d = os.path.join(WORK, "ck", "img_demo")
    out = {}
    for fn in os.listdir(d):
        if fn.endswith(".jpg"):
            with open(os.path.join(d, fn), "rb") as f:
                out[fn[:-4]] = "data:image/jpeg;base64," + base64.b64encode(f.read()).decode()
    return out


def main():
    with open(os.path.join(HERE, "template.html"), encoding="utf-8") as f:
        html = f.read()
    images = "{" + ",".join('"%s":"%s"' % (n, data_uri(n)) for n in PHOTOS) + "}"
    stamp = datetime.datetime.now().strftime("%d.%m.%Y %H:%M")
    logo = data_uri("logomark", "png")
    logo_dark = data_uri("logo", "png")
    calc = calc_uri()
    import json
    with open(os.path.join(ASSETS, "..", "cocktails.json"), encoding="utf-8") as f:
        cocktails = f.read().strip()
    ck_img = json.dumps(cocktail_images(), ensure_ascii=False)
    html = (html.replace("__IMG__", images)
                .replace("__COCKTAILS__", cocktails)
                .replace("__CK_IMG__", ck_img)
                .replace("__LOGO__", logo)
                .replace("__LOGO_DARK__", logo_dark)
                .replace("__CALC__", calc)
                .replace("__LOGO_HEADER__", logo)
                .replace("__APK__", APK_NAME)
                .replace("__ORDER_ENDPOINTS__", json.dumps(ORDER_CHANNELS, ensure_ascii=False))
                .replace("__THEME_NAME__", "a")
                .replace("__VERSION__", stamp))
    with open(os.path.join(HERE, "index.html"), "w", encoding="utf-8", newline="\n") as f:
        f.write(html)
    print("эмулятор собран:", os.path.join(HERE, "index.html"))


if __name__ == "__main__":
    main()
