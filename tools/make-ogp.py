# -*- coding: utf-8 -*-
"""
OGP画像(1200x630)を作る。

  python tools/make-ogp.py [背景画像]

背景はCodex(gpt-image-2)に描かせた文字なしのアートワーク。
文字は画像モデルに書かせず、ここで正確に載せる（漢字の字形が崩れるため）。
背景を渡さない場合は、tools/make-icons.py と同じ描き方で自前の背景を作る。
"""
from PIL import Image, ImageDraw, ImageFont
import os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT  = os.path.dirname(HERE)
W, H = 1200, 630

BLUE = (26, 79, 160); DEEP = (18, 53, 107)
TEAL = (76, 196, 184); WHITE = (255, 255, 255); DIM = (168, 190, 220)
B = r"C:\Windows\Fonts\YuGothB.ttc"
R = r"C:\Windows\Fonts\YuGothR.ttc"
f = lambda p, s: ImageFont.truetype(p, s, index=0)


def fallback_bg():
    """背景画像が無いときの自前描画。アイコンと同じ家＋脈の線。"""
    img = Image.new("RGB", (W, H), BLUE); d = ImageDraw.Draw(img)
    d.ellipse([W*0.60, -H*0.35, W*1.25, H*1.15], fill=DEEP)
    cx, cy, k = W*0.815, H*0.50, H*0.62
    pts = [(cx-k*0.62, cy+k*0.06), (cx-k*0.24, cy+k*0.06), (cx-k*0.24, cy-k*0.09),
           (cx+k*0.01, cy-k*0.36), (cx+k*0.26, cy-k*0.08), (cx+k*0.34, cy+k*0.36),
           (cx+k*0.44, cy+k*0.06), (cx+k*0.72, cy+k*0.06)]
    lw = int(H*0.055)
    d.line(pts, fill=TEAL, width=lw, joint="curve")
    for p in (pts[0], pts[-1]):
        d.ellipse([p[0]-lw/2, p[1]-lw/2, p[0]+lw/2, p[1]+lw/2], fill=TEAL)
    return img


def load_bg(path, zoom=1.10, focus_x=0.20):
    """focus_x: 横方向の切り出し位置(0=左寄せ 1=右寄せ)。
    値を小さくすると絵柄が右へ動く。左の文字と重ねないため小さめにする。"""
    im = Image.open(path).convert("RGB")
    s = max(W/im.width, H/im.height) * zoom
    im = im.resize((int(im.width*s+1), int(im.height*s+1)), Image.LANCZOS)
    x = int((im.width-W) * focus_x); y = (im.height-H)//2
    return im.crop((x, y, x+W, y+H))


src = sys.argv[1] if len(sys.argv) > 1 else None
img = load_bg(src) if src and os.path.exists(src) else fallback_bg()

# 左側に文字を置くため、左half を紺で沈める（背景の絵柄に負けないように）
veil = Image.new("RGBA", (W, H), (0, 0, 0, 0))
vd = ImageDraw.Draw(veil)
for i in range(int(W*0.74)):
    a = int(246 * min(1.0, (1 - i/(W*0.74))**0.55))
    vd.line([(i, 0), (i, H)], fill=BLUE + (a,))
img = Image.alpha_composite(img.convert("RGBA"), veil).convert("RGB")

d = ImageDraw.Draw(img)
X = 68

d.text((X, 96),  "宅建ペースメーカー", font=f(B, 60), fill=WHITE)
d.text((X, 186), "試験日まで、",        font=f(B, 44), fill=WHITE)
w = d.textlength("試験日まで、", font=f(B, 44))
d.text((X+w, 186), "今日やる10問だけ。", font=f(B, 44), fill=TEAL)
d.text((X, 262), "宅建試験の学習記録・復習支援ツール", font=f(R, 26), fill=DIM)

# 事実は実データと一致させること
facts = [("過去問",   "200問"),
         ("自作の一問一答", "190問"),
         ("論点タグ", "95種")]
for i, (label, value) in enumerate(facts):
    x = X + i * 178                                   # 等間隔に置く
    d.text((x, 340), label, font=f(R, 22), fill=DIM)
    d.text((x, 372), value, font=f(B, 40), fill=WHITE)

d.text((X, 452), "登録不要／記録はこの端末の中だけ／オフラインでも動く",
       font=f(R, 24), fill=WHITE)

d.text((X, 528), "非公式サイト｜過去問の問題文は掲載せず、公式PDFへリンクします",
       font=f(R, 21), fill=DIM)
d.text((X, 560), "一般財団法人不動産適正取引推進機構とは関係がありません",
       font=f(R, 21), fill=DIM)

path = os.path.join(OUT, "ogp.jpg")
img.save(path, "JPEG", quality=88, optimize=True)
print(f"ogp.jpg {W}x{H}  {os.path.getsize(path)} bytes")
