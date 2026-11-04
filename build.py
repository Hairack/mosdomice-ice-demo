# -*- coding: utf-8 -*-
"""Сборка эмулятора приложения «Лёд MosDomIce»: подставляет фото из приложения."""
import base64
import datetime
import io
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


def sync_version_manifest():
    """Собирает version.json из версий обоих приложений.

    Приложение на телефоне сравнивает свой номер сборки с этим файлом и
    предлагает обновиться, когда сборка на сайте новее.
    """
    import re

    android_code, android_name = 1, "1.0"
    android_file = os.path.join(ROOT, "ice-android", "app", "build.gradle.kts")
    try:
        g = io.open(android_file, encoding="utf-8").read()
        m = re.search(r"versionCode\s*=\s*(\d+)", g)
        if m:
            android_code = int(m.group(1))
        m = re.search(r'versionName\s*=\s*"([^"]+)"', g)
        if m:
            android_name = m.group(1)
    except Exception:
        pass

    ios_build, ios_name = 1, "1.0"
    ios_file = os.path.join(ROOT, "ice-app", "project.yml")
    try:
        y = io.open(ios_file, encoding="utf-8").read()
        m = re.search(r'CFBundleVersion:\s*"?(\d+)"?', y)
        if m:
            ios_build = int(m.group(1))
        m = re.search(r'CFBundleShortVersionString:\s*"([^"]+)"', y)
        if m:
            ios_name = m.group(1)
    except Exception:
        pass

    path = os.path.join(HERE, "version.json")
    notes = {"android": "", "ios": ""}
    try:
        import json as _json
        old = _json.load(io.open(path, encoding="utf-8"))
        notes["android"] = (old.get("android") or {}).get("notes", "")
        notes["ios"] = (old.get("ios") or {}).get("notes", "")
    except Exception:
        pass

    import json
    data = {
        "android": {
            "versionCode": android_code,
            "versionName": android_name,
            "url": "https://hairack.github.io/mosdomice-ice-demo/" + APK_NAME,
            "notes": notes["android"],
        },
        "ios": {
            "build": ios_build,
            "version": ios_name,
            "url": "https://hairack.github.io/mosdomice-ice-demo/update.html",
            "notes": notes["ios"],
        },
    }
    io.open(path, "w", encoding="utf-8", newline="\n").write(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n")
    print("version.json: android %s(%d), ios %s(%d)" % (android_name, android_code, ios_name, ios_build))


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
    sync_version_manifest()


if __name__ == "__main__":
    main()
