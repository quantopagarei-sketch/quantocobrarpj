"""Generic large-print word search book engine.
Usage: python3 engine.py <bookdir>                -> paperback 8.5x11 (<base>_INTERIOR.pdf, <base>_COVER.pdf)
       python3 engine.py <bookdir> --hardcover    -> hardcover 8.25x11, 80 pages (<base>_HC_INTERIOR.pdf, <base>_HC_COVER.pdf)
       python3 engine.py <bookdir> --hardcover --cover W H S
           W,H = total cover size and S = spine width in inches from KDP's cover calculator
           (if KDP rejects the cover size, regenerate with the exact numbers KDP shows).
bookdir must contain config.py with: THEMES, BOOK (dict)."""
import sys, os, json, math, random, importlib.util, re
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import Color, black, white

F = "/usr/share/fonts/truetype/dejavu/"
for n, f in [("Sans","DejaVuSans.ttf"),("SansB","DejaVuSans-Bold.ttf"),("Serif","DejaVuSerif.ttf"),("SerifB","DejaVuSerif-Bold.ttf")]:
    pdfmetrics.registerFont(TTFont(n, F+f))

N = 14
DIRS_ALL = [(0,1),(1,0),(1,1),(-1,1),(0,-1),(-1,0),(-1,-1),(1,-1)]
BAD = ["FUCK","SHIT","CUNT","DICK","COCK","PISS","SLUT","WHORE","FAG","NIGGER","NIGGA","TWAT","ANUS","PENIS","RAPE","KKK","NAZI","PORN","SEX","CUM","DAMN","HELL"]

def key(w): return re.sub(r"[^A-Z]", "", w.upper())

def dirs_for(i):
    if i < 20: return [(0,1),(1,0)]
    if i < 35: return [(0,1),(1,0),(1,1),(-1,1)]
    return DIRS_ALL

def count_occ(grid, w):
    c = 0
    for r in range(N):
        for col in range(N):
            for dr,dc in DIRS_ALL:
                ok = True
                for k,ch in enumerate(w):
                    rr,cc = r+dr*k, col+dc*k
                    if not (0<=rr<N and 0<=cc<N) or grid[rr][cc]!=ch: ok=False;break
                if ok: c+=1
    return c

def try_build(words, dirs, rng):
    grid = [[None]*N for _ in range(N)]
    placed = {}
    for w in sorted(words, key=len, reverse=True):
        opts = []
        for r in range(N):
            for c in range(N):
                for dr,dc in dirs:
                    er,ec = r+dr*(len(w)-1), c+dc*(len(w)-1)
                    if not (0<=er<N and 0<=ec<N): continue
                    ok=True
                    for k,ch in enumerate(w):
                        g = grid[r+dr*k][c+dc*k]
                        if g is not None and g!=ch: ok=False;break
                    if ok: opts.append((r,c,dr,dc))
        if not opts: return None
        r,c,dr,dc = rng.choice(opts)
        for k,ch in enumerate(w): grid[r+dr*k][c+dc*k]=ch
        placed[w]=(r,c,dr,dc)
    pool = "".join(words)
    for r in range(N):
        for c in range(N):
            if grid[r][c] is None: grid[r][c]=rng.choice(pool)
    for w in words:
        if count_occ(grid,w)!=1: return None
    for b in BAD:
        if any(b in w or b[::-1] in w for w in words): continue
        if count_occ(grid,b)>0: return None
    return grid, placed

def check(themes):
    probs=[]
    if len(themes)!=50: probs.append(("count",len(themes)))
    titles=[t for t,_ in themes]
    if len(set(titles))!=len(titles): probs.append("dup titles")
    for t,ws in themes:
        ks=[key(w) for w in ws]
        if len(ws)!=12: probs.append((t,"n",len(ws)))
        if len(set(ks))!=len(ks): probs.append((t,"dup"))
        for w in ks:
            if len(w)>N or len(w)<3: probs.append((t,w,"len"))
            if w==w[::-1]: probs.append((t,w,"palindrome"))
            for v in ks:
                if v!=w and (w in v or w[::-1] in v): probs.append((t,w,"in",v))
    return probs

def generate(themes, seed):
    rng = random.Random(seed); out=[]
    for i,(t,ws) in enumerate(themes):
        ks=[key(w) for w in ws]
        for attempt in range(3000):
            res = try_build(ks, dirs_for(i), rng)
            if res: break
        else:
            raise SystemExit(f"FAIL {t}")
        grid,placed=res
        out.append({"title":t,"display":ws,"words":ks,"grid":["".join(r) for r in grid],"placed":placed})
    return out

# ---------------- drawing ----------------
W, H = 8.5*inch, 11*inch
M = 0.75*inch
HC = False  # hardcover mode

def set_hardcover():
    global W, M, HC
    W, M, HC = 8.25*inch, 0.62*inch, True

def centered(c, txt, y, font, size, color=black, x=None):
    c.setFillColor(color); c.setFont(font, size); c.drawCentredString(W/2 if x is None else x, y, txt)

def snowflake(c, x, y, r, color):
    c.setStrokeColor(color); c.setLineWidth(max(0.6, r/10)); c.setLineCap(1)
    for k in range(6):
        a = math.pi/3*k
        c.line(x, y, x+r*math.cos(a), y+r*math.sin(a))
        bx, by = x+r*0.55*math.cos(a), y+r*0.55*math.sin(a)
        for s in (-1, 1):
            b = a + s*math.pi/4
            c.line(bx, by, bx+r*0.3*math.cos(b), by+r*0.3*math.sin(b))

def cross(c, x, y, r, color):
    c.setStrokeColor(color); c.setLineWidth(max(1, r/5)); c.setLineCap(1)
    c.line(x, y-r, x, y+r); c.line(x-r*0.6, y+r*0.35, x+r*0.6, y+r*0.35)

def dove(c, x, y, r, color):  # simple leaf/branch ornament instead
    c.setStrokeColor(color); c.setLineWidth(max(0.8, r/12)); c.setLineCap(1)
    c.line(x-r, y, x+r, y)
    for k in range(-3, 4):
        if k == 0: continue
        px = x + k*r/4
        c.ellipse(px-r*0.12, y, px+r*0.12, y+r*0.35, stroke=1, fill=0) if k%2 else c.ellipse(px-r*0.12, y-r*0.35, px+r*0.12, y, stroke=1, fill=0)

def ornament(c, kind, x, y, r, color):
    {"snow": snowflake, "cross": cross, "leaf": dove}[kind](c, x, y, r, color)

def draw_grid(c, grid, x0, ytop, cell, fsize, placed=None, words=None):
    n = len(grid)
    if placed:
        c.setStrokeColor(Color(0.78,0.78,0.78)); c.setLineCap(1); c.setLineWidth(cell*0.62)
        for w in words:
            r, col, dr, dc = placed[w]; L = len(w)-1
            c.line(x0+(col+0.5)*cell, ytop-(r+0.5)*cell, x0+(col+dc*L+0.5)*cell, ytop-(r+dr*L+0.5)*cell)
    c.setStrokeColor(black); c.setLineWidth(1.5 if not placed else 0.8)
    pad = cell*0.25
    c.roundRect(x0-pad, ytop-n*cell-pad, n*cell+2*pad, n*cell+2*pad, cell*0.3, stroke=1, fill=0)
    c.setFillColor(black); c.setFont("SansB", fsize)
    for r in range(n):
        for col in range(n):
            c.drawCentredString(x0+(col+0.5)*cell, ytop-(r+0.5)*cell-fsize*0.36, grid[r][col])

def page_number(c, n):
    c.setFont("Sans", 10); c.setFillColor(black); c.drawCentredString(W/2, 0.45*inch, str(n))

def fit_size(txt, font, size, maxw):
    while pdfmetrics.stringWidth(txt, font, size) > maxw and size > 10: size -= 1
    return size

def build_interior(B, P, out):
    c = canvas.Canvas(out, pagesize=(W, H)); c.setTitle(B["title"]); c.setAuthor(B["publisher"])
    page = 1; grey = Color(0.6,0.6,0.6); acc = Color(*B["accent"]); acc2 = Color(*B["accent2"])
    # title page
    for (x, y, r) in [(1.6,9.2,22),(6.9,9.6,16),(1.2,2.2,14),(7.2,1.8,24),(4.25,8.6,10)]:
        ornament(c, B["ornament"], x*inch, y*inch, r, grey)
    centered(c, "LARGE PRINT", 7.6*inch, "SansB", 24, acc)
    y = 6.7*inch
    for txt, font, size in B["title_lines"]:
        centered(c, txt, y, font, fit_size(txt, font, size, W-1.5*inch)); y -= size*1.25
    centered(c, B["tagline"], y-0.25*inch, "Sans", 15, acc2)
    centered(c, B["publisher"], 1.0*inch, "Sans", 13)
    c.showPage(); page += 1
    # copyright
    y = 3.2*inch
    for ln in [B["title"], "", f"Copyright © 2026 {B['publisher']}. All rights reserved.", "",
               "No part of this book may be reproduced or distributed in any form",
               "without written permission from the publisher, except for brief",
               "quotations in reviews.", "", *B.get("copyright_extra", []), "Solutions are at the back of the book."]:
        centered(c, ln, y, "Sans", 11); y -= 16
    c.showPage(); page += 1
    # how to play
    centered(c, "How to Play", 9.4*inch, "SerifB", 34)
    txt = ["Each puzzle has a list of hidden words.", "Find every word in the grid and circle it.", "",
           "Puzzles 1–20: words run left to right", "or top to bottom.", "",
           "Puzzles 21–35: words can also run diagonally.", "",
           "Puzzles 36–50: words can run in any direction,", "including backwards.", "",
           "Words with spaces or punctuation appear", "in the grid as letters only.", "",
           "All solutions are at the back of the book.", "", B["closing_line"]]
    y = 8.3*inch
    for t in txt: centered(c, t, y, "Sans", 17); y -= 27
    ornament(c, B["ornament"], W/2, 1.6*inch, 26, grey)
    page_number(c, page); c.showPage(); page += 1
    # puzzles
    cell = 0.48*inch; gx = (W - N*cell)/2
    for i, p in enumerate(P):
        centered(c, f"PUZZLE {i+1}", H-M-0.05*inch, "SansB", 13, acc)
        centered(c, p["title"], H-M-0.55*inch, "SerifB", fit_size(p["title"], "SerifB", 28, W-2*M))
        ytop = H-M-0.95*inch
        draw_grid(c, p["grid"], gx, ytop, cell, 21)
        words = p["display"]; cols = 3; rows = 4; colw = (W-2*M)/cols
        y0 = ytop - N*cell - 0.55*inch
        for k, w in enumerate(words):
            col, row = k // rows, k % rows
            x = M + col*colw + 0.15*inch; yy = y0 - row*0.34*inch
            fs = fit_size(w, "Sans", 16, colw-0.38*inch)
            if fs < 16: raise SystemExit(f"word too long for large print: {w}")
            c.setFont("Sans", 16); c.setFillColor(black)
            c.rect(x, yy-1, 9, 9, stroke=1, fill=0); c.drawString(x+16, yy, w)
        page_number(c, page); c.showPage(); page += 1
    # solutions
    centered(c, "Solutions", H/2+0.2*inch, "SerifB", 40)
    ornament(c, B["ornament"], W/2, H/2-0.8*inch, 24, grey)
    page_number(c, page); c.showPage(); page += 1
    if HC:  # bigger solution grids, 2 per page (also brings the book to 80 pages, KDP hardcover minimum is 75)
        scell = 0.3*inch; gw = N*scell; sfs = 12.5
        positions = [((W-gw)/2, H-M-0.35*inch), ((W-gw)/2, H/2-0.35*inch)]
    else:
        scell = 0.235*inch; gw = N*scell; sfs = 9.5
        positions = [(M+0.1*inch, H-M-0.45*inch), (W-M-0.1*inch-gw, H-M-0.45*inch),
                     (M+0.1*inch, H/2-0.15*inch), (W-M-0.1*inch-gw, H/2-0.15*inch)]
    per = len(positions)
    for start in range(0, len(P), per):
        for j, (x, yt) in enumerate(positions):
            k = start + j
            if k >= len(P): break
            p = P[k]; lbl = f"{k+1}. {p['title']}"
            c.setFont("SansB", fit_size(lbl, "SansB", 14 if HC else 12, gw+0.3*inch)); c.setFillColor(black)
            c.drawCentredString(x+gw/2, yt+0.15*inch, lbl)
            draw_grid(c, p["grid"], x, yt-0.05*inch, scell, sfs, placed=p["placed"], words=p["words"])
        page_number(c, page); c.showPage(); page += 1
    # thank you
    centered(c, "Thank You!", 7.2*inch, "SerifB", 40)
    for t, yy in [("We hope these puzzles brought you", 6.2), (B["thanks_line"], 5.85),
                  ("If you enjoyed this book, a short review", 5.1), ("on Amazon would mean the world to us.", 4.75),
                  (B["signoff"], 3.9)]:
        centered(c, t, yy*inch, "Sans", 17)
    ornament(c, B["ornament"], W/2, 2.6*inch, 30, grey)
    page_number(c, page); c.showPage(); page += 1
    if (page-1) % 2: c.showPage(); page += 1
    c.save(); return page-1

def build_cover(B, pages, out, override=None):
    if HC:
        # Case laminate: 0.591in wrap, board = trim + 0.197in (w) / + 0.236in (h),
        # spine = pages*0.002252 + 0.189in (matches KDP cover calculator; override with its exact numbers)
        TW, TH = 8.25*inch, 11*inch; OUT = 0.591*inch
        PW = TW + 0.197*inch
        SPINE = (pages*0.002252 + 0.189)*inch
        CW, CH = 2*OUT + 2*PW + SPINE, 2*OUT + TH + 0.236*inch
        if override:
            CW, CH, SPINE = override[0]*inch, override[1]*inch, override[2]*inch
            PW = (CW - SPINE)/2 - OUT
        SAFE = 0.75*inch  # text kept >= 0.635in from the board edge and clear of the 0.4in hinge
    else:
        TW, TH = 8.5*inch, 11*inch; OUT = 0.125*inch; PW = TW
        SPINE = pages*0.002252*inch
        CW, CH = 2*OUT + 2*TW + SPINE, TH + 2*OUT
        SAFE = 0.45*inch
    BLEED = (CH - TH)/2  # vertical offset of the 11in design area
    bg = Color(*B["cover_bg"]); dark = Color(*B["cover_dark"]); band = Color(*B["cover_band"])
    gold = Color(*B["cover_gold"]); cream = Color(0.99,0.97,0.92); deco = Color(1,1,1,alpha=0.16)
    c = canvas.Canvas(out, pagesize=(CW, CH))
    c.setFillColor(bg); c.rect(0, 0, CW, CH, stroke=0, fill=1)
    rng = random.Random(7)
    for _ in range(B.get("cover_deco_count", 70)):
        ornament(c, B["ornament"], rng.uniform(0, CW), rng.uniform(0, CH), rng.uniform(6, 24), deco)
    fx = OUT + PW + SPINE; cx = fx + PW/2
    c.setFillColor(band); c.rect(fx, BLEED+9.0*inch, PW+OUT, 1.0*inch, stroke=0, fill=1)
    centered(c, "LARGE PRINT", BLEED+9.33*inch, "SansB", 40, white, x=cx)
    y = BLEED + 7.65*inch
    for txt, size, colr in B["cover_lines"]:
        font = "SerifB" if colr != "gold" else "Serif"
        s = fit_size(txt, font, size, PW-2*SAFE)
        centered(c, txt, y, font, s, gold if colr=="gold" else white, x=cx); y -= max(s*0.9, 0.75*inch)
    # mini grid
    gsz, cell = 7, 0.42*inch
    gx0 = cx - gsz*cell/2; gy0 = BLEED + 2.55*inch
    c.setFillColor(cream); c.roundRect(gx0-0.2*inch, gy0-0.2*inch, gsz*cell+0.4*inch, gsz*cell+0.4*inch, 12, stroke=0, fill=1)
    hw = B["cover_word"]
    c.setFillColor(Color(0.98,0.85,0.5)); c.roundRect(gx0+0.05*inch, gy0+3*cell+0.06*inch, len(hw)*cell-0.1*inch, cell-0.12*inch, 8, stroke=0, fill=1)
    letters = B["cover_letters"]; k = 0
    for r in range(gsz):
        for col in range(gsz):
            ch = letters[k % len(letters)]; k += 1
            if r == 3 and col < len(hw): ch = hw[col]
            c.setFillColor(dark); c.setFont("SansB", 18)
            c.drawCentredString(gx0+(col+0.5)*cell, gy0+(gsz-1-r)*cell+cell*0.32, ch)
    bx, by = fx + PW - (SAFE + 0.85*inch if HC else 1.25*inch), BLEED + 4.75*inch
    c.setFillColor(band); c.circle(bx, by, 0.85*inch, stroke=0, fill=1)
    c.setStrokeColor(gold); c.setLineWidth(3); c.circle(bx, by, 0.77*inch, stroke=1, fill=0)
    centered(c, "50", by+0.02*inch, "SansB", 34, white, x=bx)
    centered(c, "PUZZLES", by-0.28*inch, "SansB", 13, white, x=bx)
    tl = "Big, Easy-to-Read Letters • Solutions Included"
    centered(c, tl, BLEED+1.55*inch, "Sans", fit_size(tl, "Sans", 19, PW-2*SAFE), white, x=cx)
    centered(c, B["publisher"], BLEED+0.85*inch, "Sans", 14, gold, x=cx)
    # back
    bcx = OUT + PW/2; bx0 = bcx - TW/2
    c.setFillColor(cream); c.roundRect(bx0+0.9*inch, BLEED+3.2*inch, TW-1.8*inch, 6.4*inch, 18, stroke=0, fill=1)
    y = BLEED+8.7*inch
    for ln in B["back_head"]:
        centered(c, ln, y, "SerifB", 30, dark, x=bcx); y -= 0.55*inch
    y = BLEED+7.4*inch; c.setFillColor(dark); c.setFont("Sans", 15)
    for ln in B["back_body"]:
        if HC: ln = ln.replace("8.5 x 11", "8.25 x 11").replace("8.5x11", "8.25x11")
        c.drawString(bx0+1.35*inch, y, ln); y -= 0.3*inch
    c.save()

if __name__ == "__main__":
    d = sys.argv[1]
    override = None
    if "--hardcover" in sys.argv:
        set_hardcover()
        if "--cover" in sys.argv:
            i = sys.argv.index("--cover"); override = [float(v) for v in sys.argv[i+1:i+4]]
    spec = importlib.util.spec_from_file_location("cfg", os.path.join(d, "config.py"))
    cfg = importlib.util.module_from_spec(spec); spec.loader.exec_module(cfg)
    probs = check(cfg.THEMES)
    if probs: print("PROBLEMS:", probs); sys.exit(1)
    P = generate(cfg.THEMES, cfg.BOOK["seed"])
    json.dump(P, open(os.path.join(d, "puzzles.json"), "w"))
    base = cfg.BOOK["file_base"] + ("_HC" if HC else "")
    pages = build_interior(cfg.BOOK, P, os.path.join(d, base+"_INTERIOR.pdf"))
    if HC and pages < 75: raise SystemExit(f"hardcover needs 75+ pages, got {pages}")
    build_cover(cfg.BOOK, pages, os.path.join(d, base+"_COVER.pdf"), override)
    print("OK", "hardcover" if HC else "paperback", "pages", pages)
