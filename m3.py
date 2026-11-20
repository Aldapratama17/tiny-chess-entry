import json, os, sys, urllib.request
from random import Random
ai = os.environ.get('MAKEFUN_ENV_URL') or sys.exit('MAKEFUN_ENV_URL is not set')
def be(bf, bk):
    bp = urllib.request.Request(ai + bf, data=json.dumps(bk).encode(), headers={'content-type': 'application/json'})
    return json.load(urllib.request.urlopen(bp))
do = (-21, -19, -12, -8, 8, 12, 19, 21)
dp = (-11, -10, -9, -1, 1, 9, 10, 11)
ec = (-11, -9, 9, 11)
dn = (-10, -1, 1, 10)
eg, ee, eb, dz, dx, dv, dt, dr = (91, 92, 93, 94, 95, 96, 97, 98)
ef, ed, ea, dy, dw, du, ds, dq = (21, 22, 23, 24, 25, 26, 27, 28)
def o(by):
    n, side, castle, ep, half = by.split()[:5]
    b = [' '] * 120
    for r in range(8):
        for c in range(8):
            b[21 + r * 10 + c] = '.'
    r = c = 0
    for dg in n:
        if dg == '/':
            r += 1
            c = 0
        elif dg.isdigit():
            c += int(dg)
        else:
            b[21 + r * 10 + c] = dg
            c += 1
    ep = None if ep == '-' else 21 + (8 - int(ep[1])) * 10 + (ord(ep[0]) - 97)
    return (b, side, castle, ep, int(half))
ce = Random(12345)
ao = 'PNBRQKpnbrqk'
dl = {p: [ce.getrandbits(64) for _ in range(120)] for p in ao}
dk = ce.getrandbits(64)
dm = {c: ce.getrandbits(64) for c in 'KQkq'}
cc = {f: ce.getrandbits(64) for f in range(120)}
def ak(b, side, castle, ep):
    h = 0
    for cq in range(21, 99):
        p = b[cq]
        if p != ' ' and p != '.':
            h ^= dl[p][cq]
    h ^= dk if side == 'w' else 0
    for c in castle.replace('-', ''):
        h ^= dm[c]
    if ep is not None:
        h ^= cc[ep]
    return h
def q(b, side, castle, ep, w=False):
    cz = []
    bs = str.isupper if side == 'w' else str.islower
    for cq in range(21, 99):
        p = b[cq]
        if p == ' ' or p == '.' or (not bs(p)):
            continue
        da = p.lower()
        if da == 'p':
            d = -10 if side == 'w' else 10
            l = 2 if side == 'w' else 9
            bu = cq + d
            if b[bu] == '.' and (not w):
                if bu // 10 == l:
                    for cw in 'qrbn':
                        cz.append((cq, bu, cw, 0))
                else:
                    cz.append((cq, bu, None, 0))
                    j = 8 if side == 'w' else 3
                    if cq // 10 == j and b[cq + 2 * d] == '.':
                        cz.append((cq, cq + 2 * d, None, 0))
            for de in (d - 1, d + 1):
                t = cq + de
                if b[t] == ' ':
                    continue
                cj = b[t]
                if ep is not None and t == ep:
                    cz.append((cq, t, None, 1))
                elif cj != '.' and (not bs(cj)):
                    if t // 10 == l:
                        for cw in 'qrbn':
                            cz.append((cq, t, cw, 0))
                    else:
                        cz.append((cq, t, None, 0))
        elif da == 'n':
            for d in do:
                t = cq + d
                cj = b[t]
                if cj == ' ':
                    continue
                if cj == '.':
                    if not w:
                        cz.append((cq, t, None, 0))
                elif not bs(cj):
                    cz.append((cq, t, None, 0))
        elif da == 'k':
            for d in dp:
                t = cq + d
                cj = b[t]
                if cj == ' ':
                    continue
                if cj == '.':
                    if not w:
                        cz.append((cq, t, None, 0))
                elif not bs(cj):
                    cz.append((cq, t, None, 0))
            if not w:
                if side == 'w':
                    if 'K' in castle and b[dv] == '.' and (b[dt] == '.') and (b[dx] == 'K') and (b[dr] == 'R'):
                        cz.append((dx, dt, None, 2))
                    if 'Q' in castle and b[dz] == '.' and (b[eb] == '.') and (b[ee] == '.') and (b[dx] == 'K') and (b[eg] == 'R'):
                        cz.append((dx, eb, None, 2))
                else:
                    if 'k' in castle and b[du] == '.' and (b[ds] == '.') and (b[dw] == 'k') and (b[dq] == 'r'):
                        cz.append((dw, ds, None, 2))
                    if 'q' in castle and b[dy] == '.' and (b[ea] == '.') and (b[ed] == '.') and (b[dw] == 'k') and (b[ef] == 'r'):
                        cz.append((dw, ea, None, 2))
        else:
            bj = ec if da == 'b' else dn if da == 'r' else dp
            for d in bj:
                t = cq + d
                while b[t] != ' ':
                    cj = b[t]
                    if cj == '.':
                        if not w:
                            cz.append((cq, t, None, 0))
                    elif not bs(cj):
                        cz.append((cq, t, None, 0))
                        break
                    else:
                        break
                    t += d
    return cz
cd = dict(zip('pnbrqk', (100, 320, 330, 500, 900, 0)))
def ac(b, cq, ab):
    da = 'pnbrqk' if ab else 'PNBRQK'
    for d in do:
        if b[cq + d] == ('N' if ab else 'n'):
            return True
    for d in dp:
        if b[cq + d] == ('K' if ab else 'k'):
            return True
    cx = 10 if ab else -10
    for d in (cx - 1, cx + 1):
        if b[cq + d] == ('P' if ab else 'p'):
            return True
    for d in ec:
        t = cq + d
        while b[t] != ' ':
            p = b[t]
            if p != '.':
                if p in ('B', 'b') or p in ('Q', 'q'):
                    if p.isupper() == ab:
                        return True
                break
            t += d
    for d in dn:
        t = cq + d
        while b[t] != ' ':
            p = b[t]
            if p != '.':
                if p in ('R', 'r') or p in ('Q', 'q'):
                    if p.isupper() == ab:
                        return True
                break
            t += d
    return False
class cf:
    x = ('b', 'side', 'castle', 'ep', 'half', 'key', 'hist')
    def __init__(bb, by):
        bb.b, bb.side, bb.castle, bb.ep, bb.half = o(by)
        bb.key = ak(bb.b, bb.side, bb.castle, bb.ep)
        bb.hist = []
    def moves(bb, w=False):
        return q(bb.b, bb.side, bb.castle, bb.ep, w)
    def make(bb, m):
        bx, ck, ar, bi = m
        b = bb.b
        p = b[bx]
        bz = b[ck]
        co = (bx, ck, p, bz, bb.castle, bb.ep, bb.half, bb.key)
        bb.hist.append(co)
        bb.key ^= dl[p][bx] ^ dk
        if bz != '.':
            bb.key ^= dl[bz][ck]
        bg = (ar.upper() if bb.side == 'w' else ar) if ar else p
        b[ck] = bg
        b[bx] = '.'
        bb.key ^= dl[bg][ck]
        bb.ep = None
        z = 1
        if p.lower() == 'p' or bz != '.':
            z = 0
        bb.half = bb.half + z
        if bi == 1:
            am = ck + (10 if bb.side == 'w' else -10)
            df = b[am]
            bb.key ^= dl[df][am]
            b[am] = '.'
        elif bi == 2:
            if ck == dt:
                ct, cr, cs = (dr, dv, 'R')
            elif ck == eb:
                ct, cr, cs = (eg, dz, 'R')
            elif ck == ds:
                ct, cr, cs = (dq, du, 'r')
            else:
                ct, cr, cs = (ef, dy, 'r')
            b[ct] = '.'
            b[cr] = cs
            bb.key ^= dl[cs][ct] ^ dl[cs][cr]
        elif p.lower() == 'p' and abs(ck - bx) == 20:
            bb.ep = (bx + ck) // 2
            bb.key ^= cc[bb.ep]
        for c, cq in (('K', dr), ('Q', eg), ('k', dq), ('q', ef)):
            if c in bb.castle and (bx == cq or ck == cq or (p in 'Kk' and bx == (dx if c in 'KQ' else dw))):
                bb.castle = bb.castle.replace(c, '')
                bb.key ^= dm[c]
        bb.side = 'b' if bb.side == 'w' else 'w'
        bb.key ^= dk
    def unmake(bb):
        bx, ck, p, bz, castle, ep, half, key = bb.hist.pop()
        b = bb.b
        b[bx] = p
        b[ck] = bz
        if p.lower() == 'p' and ck == ep and (bz == '.'):
            am = ck + (10 if p == 'P' else -10)
            b[am] = 'p' if p == 'P' else 'P'
        y = 'b' if bb.side == 'w' else 'w'
        if p in 'Kk' and abs(ck - bx) == 2:
            if ck == dt:
                b[dr], b[dv] = ('R', '.')
            elif ck == eb:
                b[eg], b[dz] = ('R', '.')
            elif ck == ds:
                b[dq], b[du] = ('r', '.')
            else:
                b[ef], b[dy] = ('r', '.')
        bb.castle, bb.ep, bb.half, bb.key = (castle, ep, half, key)
        bb.side = y
    def king_sq(bb, side):
        k = 'K' if side == 'w' else 'k'
        return bb.b.index(k) if k in bb.b else -1
    def in_check(bb, side=None):
        side = side or bb.side
        return ac(bb.b, bb.king_sq(side), side == 'b')
def ah(a, b):
    cv, di = (a // 10, a % 10)
    cu, dh = (b // 10, b % 10)
    return cv == cu or di == dh or abs(cv - cu) == abs(di - dh)
def i(bq):
    bt = []
    av = bq.side
    bw = bq.king_sq(av)
    bc = not bq.in_check(side=av)
    for m in bq.moves():
        if m[3] == 2:
            bh = dx if m[1] in (dt, eb) else dw
            bv = (dv, dt) if m[1] == dt else (dz, eb) if m[1] == eb else (du, ds) if m[1] == ds else (dy, ea)
            if any((ac(bq.b, s, av == 'b') for s in (bh,) + bv)):
                continue
        if bc and bq.b[m[0]] not in 'Kk' and (m[3] != 1) and (not ah(m[0], bw)):
            bt.append(m)
            continue
        bq.make(m)
        if not bq.in_check(side=av):
            bt.append(m)
        bq.unmake()
    return bt
cg = {'p': (0, 0, 0, 0, 0, 0, 0, 0, 60, 60, 60, 60, 60, 60, 60, 60, 12, 18, 24, 30, 30, 24, 18, 12, 6, 10, 16, 26, 26, 16, 10, 6, 2, 4, 10, 22, 22, 10, 4, 2, 2, -2, -4, 4, 4, -4, -2, 2, 2, 4, 4, -8, -8, 4, 4, 2, 0, 0, 0, 0, 0, 0, 0, 0), 'n': (-40, -28, -18, -18, -18, -18, -28, -40, -24, -12, 0, 4, 4, 0, -12, -24, -14, 2, 10, 10, 10, 10, 2, -14, -10, 6, 14, 16, 16, 14, 6, -10, -10, 4, 14, 16, 16, 14, 4, -10, -16, 0, 10, 12, 12, 10, 0, -16, -26, -14, 0, 2, 2, 0, -14, -26, -46, -30, -20, -18, -18, -20, -30, -46), 'b': (-16, -8, -8, -8, -8, -8, -8, -16, -8, 2, 0, 0, 0, 0, 2, -8, -6, 4, 6, 8, 8, 6, 4, -6, -4, 6, 10, 12, 12, 10, 6, -4, -4, 8, 10, 12, 12, 10, 8, -4, -6, 10, 8, 8, 8, 8, 10, -6, -8, 10, 6, 4, 4, 6, 10, -8, -14, -8, -10, -8, -8, -10, -8, -14), 'r': (0, 0, 0, 0, 0, 0, 0, 0, 4, 8, 8, 8, 8, 8, 8, 4, -4, 0, 0, 0, 0, 0, 0, -4, -4, 0, 0, 0, 0, 0, 0, -4, -4, 0, 0, 0, 0, 0, 0, -4, -4, 0, 0, 0, 0, 0, 0, -4, -4, 0, 0, 0, 0, 0, 0, -4, 0, 0, 4, 8, 8, 4, 0, 0), 'k': (-50, -40, -30, -20, -20, -30, -40, -50, -36, -24, -12, 0, 0, -12, -24, -36, -26, -12, 10, 20, 20, 10, -12, -26, -16, 4, 18, 26, 26, 18, 4, -16, -8, 10, 22, 30, 30, 22, 10, -8, -4, 14, 26, 36, 36, 26, 14, -4, -4, 10, 16, 20, 20, 16, 10, -4, -10, -6, 0, 10, 10, 0, -6, -10)}
def aj(cq):
    r = cq // 10 - 2
    c = cq % 10 - 1
    return (r, c)
def aa(bq):
    b = bq.b
    aq = 0
    for cq in range(21, 99):
        p = b[cq]
        if p == ' ' or p == '.':
            continue
        da = p.lower()
        r, c = aj(cq)
        v = cd[da] + (cg[da][r * 8 + c if p.isupper() else (7 - r) * 8 + c] if da in cg else 0)
        if p.isupper():
            aq += v
        else:
            aq -= v
    return aq if bq.side == 'w' else -aq
bn = 100000
e = 50000
class ba(Exception):
    pass
def bd(bq, moves, ay, at, an, ci, ae):
    az = -bn
    bm = None
    moves = [ae] + [m for m in moves if m != ae]
    for m in moves:
        bq.make(m)
        v = -ag(bq, ay - 1, -bn, -az, at, an, ci, 1)
        bq.unmake()
        if v > az:
            az = v
            bm = m
    return bm if bm else moves[0]
def ag(bq, ay, az, bl, at, an, ci, br):
    at[0] += 1
    if at[0] > an:
        raise ba()
    if bq.half >= 100:
        return 0
    al = bq.in_check()
    if al:
        ay += 1
    if ay <= 0:
        return af(bq, az, bl, at, an)
    key = bq.key
    ax = ci.get(key)
    ad = ax[3] if ax else None
    if not al and ay >= 3:
        cn = (bq.side, bq.ep, bq.key)
        bq.side = 'b' if bq.side == 'w' else 'w'
        bq.key ^= dk ^ (cc[bq.ep] if bq.ep else 0)
        bq.ep = None
        cy = -ag(bq, ay - 3, -bl, -bl + 1, at, an, ci, br + 1)
        bq.side, bq.ep, bq.key = cn
        if cy >= bl:
            return cy
    moves = i(bq)
    if not moves:
        return -bn + br if al else 0
    if ax and ax[0] >= ay:
        s, bi = (ax[1], ax[2])
        if bi == 0:
            return s
        if bi == 1 and s >= bl:
            return s
        if bi == 2 and s <= az:
            return s
    def au(m):
        if ad and m == ad:
            return 1 << 30
        bz = bq.b[m[1]]
        if bz != '.':
            return (1 << 20) + cd[bz.lower()] * 10 - cd[bq.b[m[0]].lower()]
        if m[2]:
            return (1 << 20) - 1000
        dc, cm = (aj(m[0]), aj(m[1]))
        cl = cg.get(bq.b[m[0]].lower())
        if cl:
            return cl[cm[0] * 8 + cm[1]] - cl[dc[0] * 8 + dc[1]] if bq.side == 'w' else cl[(7 - cm[0]) * 8 + cm[1]] - cl[(7 - dc[0]) * 8 + dc[1]]
        return 0
    moves.sort(key=au, reverse=True)
    bm = -bn
    dj = az
    for m in moves:
        bq.make(m)
        v = -ag(bq, ay - 1, -bl, -az, at, an, ci, br + 1)
        bq.unmake()
        if v > bm:
            bm = v
            if v > az:
                az = v
        if az >= bl:
            break
    bi = 0
    if bm <= dj:
        bi = 2
    elif bm >= bl:
        bi = 1
    ci[key] = (ay, bm, bi, moves[0])
    return bm
def af(bq, az, bl, at, an, d=0):
    at[0] += 1
    if at[0] > an:
        raise ba()
    if d > 8:
        return aa(bq)
    ap = aa(bq)
    if ap >= bl:
        return ap
    if ap + 950 < az:
        return ap
    if ap > az:
        az = ap
    av = bq.side
    for m in bq.moves(w=True):
        bz = bq.b[m[1]]
        if ap + cd[bz.lower() if bz != '.' else 'p'] + 200 <= az:
            continue
        bq.make(m)
        if bq.in_check(side=av):
            bq.unmake()
            continue
        v = -af(bq, -bl, -az, at, an, d + 1)
        bq.unmake()
        if v >= bl:
            return v
        if v > az:
            az = v
    return az
def bo(m):
    f, t, ar, bi = m
    db = lambda s: chr(97 + (s % 10 - 1)) + str(8 - (s // 10 - 2))
    return db(f) + db(t) + (ar or '')
def main():
    g = be('/game', {})
    while g.get('status') != 'done':
        if g.get('status') == 'your_move':
            bq = cf(g['fen'])
            aw = set(g['legal_moves'])
            ci = {}
            at = [0]
            moves = i(bq)
            moves = [m for m in moves if bo(m) in aw] or moves
            bm = moves[0] if moves else None
            if bm:
                for ay in range(1, 64):
                    try:
                        bm = bd(bq, moves, ay, at, e, ci, bm)
                    except ba:
                        break
                    moves = [bm] + [m for m in moves if m != bm]
                u = bo(bm)
            else:
                u = sorted(aw)[0]
            if u not in aw:
                u = min(aw)
            g = be('/move', {'game': g['game'], 'move': u})
        else:
            g = be('/game', {})
    sys.stderr.write(json.dumps({'wins': g.get('wins'), 'draws': g.get('draws'), 'losses': g.get('losses')}))
if __name__ == '__main__':
    main()