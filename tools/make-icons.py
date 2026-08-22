# -*- coding: utf-8 -*-
"""
宅建ペースメーカーのアイコンを生成する。

  python tools/make-icons.py

紺地に、ティールの線が1本。左から水平に来て家の切妻屋根の形に立ち上がり、
そこから心電図のように急降下して戻る。「家」と「脈」を1本の線で兼ねている。

Pillow だけで完結する。フォントも外部アセットも要らない。
色はアプリ本体の CSS 変数（--blue / --teal）と揃えてある。
"""
from PIL import Image, ImageDraw
import os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT  = os.path.dirname(HERE)

BLUE = (26, 79, 160)     # --blue  #1a4fa0
TEAL = (76, 196, 184)    # 濃紺の上で映えるティール
S    = 1024              # 原寸。各サイズへ縮小する


def icon(pad=0.0, stroke=0.062):
    """pad: マスカブル用に中身を内側へ寄せる割合（0.0〜0.3）"""
    img = Image.new("RGB", (S, S), BLUE)
    d = ImageDraw.Draw(img)
    k = 1.0 - pad
    P = lambda t: S * (0.5 + (t - 0.5) * k)   # 中心から縮める
    lw = max(2, int(S * stroke * k))

    pts = [
        (P(0.070), P(0.535)),   # 左の水平線
        (P(0.300), P(0.535)),
        (P(0.300), P(0.445)),   # 家の左の壁
        (P(0.455), P(0.285)),   # 屋根の頂点
        (P(0.605), P(0.452)),   # 屋根の右斜面
        (P(0.655), P(0.715)),   # 脈の落ち込み
        (P(0.715), P(0.535)),
        (P(0.930), P(0.535)),   # 右の水平線
    ]
    d.line(pts, fill=TEAL, width=lw, joint="curve")
    for p in (pts[0], pts[-1]):               # 端を丸める
        d.ellipse([p[0]-lw/2, p[1]-lw/2, p[0]+lw/2, p[1]+lw/2], fill=TEAL)
    return img


base = icon()
mask = icon(pad=0.20)                          # 端を切られても中身が残る
tiny = icon(stroke=0.085)                      # 小さいと線が消えるので太らせる

TARGETS = [
    ("icon-512.png",          base, 512),
    ("icon-192.png",          base, 192),
    ("icon-maskable-512.png", mask, 512),
    ("apple-touch-icon.png",  base, 180),      # iOSのホーム画面はこれを見る
    ("favicon-32.png",        tiny, 32),
]

for name, img, px in TARGETS:
    path = os.path.join(OUT, name)
    img.resize((px, px), Image.LANCZOS).save(path, optimize=True)
    print(f"{name:24s} {px}x{px}  {os.path.getsize(path)} bytes")
