import json, os, sys, urllib.request
from random import Random
aj = os.environ.get('MAKEFUN_ENV_URL') or sys.exit('MAKEFUN_ENV_URL is not set')
def bg(bh, bm):
    br = urllib.request.Request(aj + bh, data=json.dumps(bm).encode(), headers={'content-type': 'application/json'})
    return json.load(urllib.request.urlopen(br))
dq = (-21, -19, -12, -8, 8, 12, 19, 21)
dr = (-11, -10, -9, -1, 1, 9, 10, 11)
ee = (-11, -9, 9, 11)
dp = (-10, -1, 1, 10)
ei, eg, ed, eb, dz, dx, dv, dt = (91, 92, 93, 94, 95, 96, 97, 98)
eh, ef, ec, ea, dy, dw, du, ds = (21, 22, 23, 24, 25, 26, 27, 28)
def o(cc):
    n, side, castle, ep, half = cc.split()[:5]
    b = [' '] * 120
    for r in range(8):
        for c in range(8):
            b[21 + r * 10 + c] = '.'
    r = c = 0
    for di in n:
        if di == '/':
            r += 1
            c = 0
        elif di.isdigit():
            c += int(di)
        else:
            b[21 + r * 10 + c] = di
            c += 1
    ep = None if ep == '-' else 21 + (8 - int(ep[1])) * 10 + (ord(ep[0]) - 97)
    return (b, side, castle, ep, int(half))
cg = Random(12345)
ap = 'PNBRQKpnbrqk'
dn = {p: [cg.getrandbits(64) for _ in range(120)] for p in ap}
dm = cg.getrandbits(64)
do = {c: cg.getrandbits(64) for c in 'KQkq'}
ce = {f: cg.getrandbits(64) for f in range(120)}
def al(b, side, castle, ep):
    h = 0
    for cs in range(21, 99):
        p = b[cs]
        if p != ' ' and p != '.':
            h ^= dn[p][cs]
    h ^= dm if side == 'w' else 0
    for c in castle.replace('-', ''):
        h ^= do[c]
    if ep is not None:
        h ^= ce[ep]
    return h
def q(b, side, castle, ep, w=False):
    db = []
    bu = str.isupper if side == 'w' else str.islower
    for cs in range(21, 99):
        p = b[cs]
        if p == ' ' or p == '.' or (not bu(p)):
            continue
        dc = p.lower()
        if dc == 'p':
            d = -10 if side == 'w' else 10
            l = 2 if side == 'w' else 9
            bw = cs + d
            if b[bw] == '.' and (not w):
                if bw // 10 == l:
                    for cy in 'qrbn':
                        db.append((cs, bw, cy, 0))
                else:
                    db.append((cs, bw, None, 0))
                    j = 8 if side == 'w' else 3
                    if cs // 10 == j and b[cs + 2 * d] == '.':
                        db.append((cs, cs + 2 * d, None, 0))
            for dg in (d - 1, d + 1):
                t = cs + dg
                if b[t] == ' ':
                    continue
                cl = b[t]
                if ep is not None and t == ep:
                    db.append((cs, t, None, 1))
                elif cl != '.' and (not bu(cl)):
                    if t // 10 == l:
                        for cy in 'qrbn':
                            db.append((cs, t, cy, 0))
                    else:
                        db.append((cs, t, None, 0))
        elif dc == 'n':
            for d in dq:
                t = cs + d
                cl = b[t]
                if cl == ' ':
                    continue
                if cl == '.':
                    if not w:
                        db.append((cs, t, None, 0))
                elif not bu(cl):
                    db.append((cs, t, None, 0))
        elif dc == 'k':
            for d in dr:
                t = cs + d
                cl = b[t]
                if cl == ' ':
                    continue
                if cl == '.':
                    if not w:
                        db.append((cs, t, None, 0))
                elif not bu(cl):
                    db.append((cs, t, None, 0))
            if not w:
                if side == 'w':
                    if 'K' in castle and b[dx] == '.' and (b[dv] == '.') and (b[dz] == 'K') and (b[dt] == 'R'):
                        db.append((dz, dv, None, 2))
                    if 'Q' in castle and b[eb] == '.' and (b[ed] == '.') and (b[eg] == '.') and (b[dz] == 'K') and (b[ei] == 'R'):
                        db.append((dz, ed, None, 2))
                else:
                    if 'k' in castle and b[dw] == '.' and (b[du] == '.') and (b[dy] == 'k') and (b[ds] == 'r'):
                        db.append((dy, du, None, 2))
                    if 'q' in castle and b[ea] == '.' and (b[ec] == '.') and (b[ef] == '.') and (b[dy] == 'k') and (b[eh] == 'r'):
                        db.append((dy, ec, None, 2))
        else:
            bl = ee if dc == 'b' else dp if dc == 'r' else dr
            for d in bl:
                t = cs + d
                while b[t] != ' ':
                    cl = b[t]
                    if cl == '.':
                        if not w:
                            db.append((cs, t, None, 0))
                    elif not bu(cl):
                        db.append((cs, t, None, 0))
                        break
                    else:
                        break
                    t += d
    return db
cf = dict(zip('pnbrqk', (100, 320, 330, 500, 900, 0)))
def ac(b, cs, ab):
    dc = 'pnbrqk' if ab else 'PNBRQK'
    for d in dq:
        if b[cs + d] == ('N' if ab else 'n'):
            return True
    for d in dr:
        if b[cs + d] == ('K' if ab else 'k'):
            return True
    cz = 10 if ab else -10
    for d in (cz - 1, cz + 1):
        if b[cs + d] == ('P' if ab else 'p'):
            return True
    for d in ee:
        t = cs + d
        while b[t] != ' ':
            p = b[t]
            if p != '.':
                if p in ('B', 'b') or p in ('Q', 'q'):
                    if p.isupper() == ab:
                        return True
                break
            t += d
    for d in dp:
        t = cs + d
        while b[t] != ' ':
            p = b[t]
            if p != '.':
                if p in ('R', 'r') or p in ('Q', 'q'):
                    if p.isupper() == ab:
                        return True
                break
            t += d
    return False
class ci:
    x = ('b', 'side', 'castle', 'ep', 'half', 'key', 'hist')
    def __init__(bc, cc):
        bc.b, bc.side, bc.castle, bc.ep, bc.half = o(cc)
        bc.key = al(bc.b, bc.side, bc.castle, bc.ep)
        bc.hist = []
    def moves(bc, w=False):
        return q(bc.b, bc.side, bc.castle, bc.ep, w)
    def make(bc, m):
        bz, cm, at, bk = m
        b = bc.b
        p = b[bz]
        cd = b[cm]
        cr = (bz, cm, p, cd, bc.castle, bc.ep, bc.half, bc.key)
        bc.hist.append(cr)
        bc.key ^= dn[p][bz] ^ dm
        if cd != '.':
            bc.key ^= dn[cd][cm]
        bi = (at.upper() if bc.side == 'w' else at) if at else p
        b[cm] = bi
        b[bz] = '.'
        bc.key ^= dn[bi][cm]
        bc.ep = None
        z = 1
        if p.lower() == 'p' or cd != '.':
            z = 0
        bc.half = bc.half + z
        if bk == 1:
            an = cm + (10 if bc.side == 'w' else -10)
            dh = b[an]
            bc.key ^= dn[dh][an]
            b[an] = '.'
        elif bk == 2:
            if cm == dv:
                cv, ct, cu = (dt, dx, 'R')
            elif cm == ed:
                cv, ct, cu = (ei, eb, 'R')
            elif cm == du:
                cv, ct, cu = (ds, dw, 'r')
            else:
                cv, ct, cu = (eh, ea, 'r')
            b[cv] = '.'
            b[ct] = cu
            bc.key ^= dn[cu][cv] ^ dn[cu][ct]
        elif p.lower() == 'p' and abs(cm - bz) == 20:
            bc.ep = (bz + cm) // 2
            bc.key ^= ce[bc.ep]
        for c, cs in (('K', dt), ('Q', ei), ('k', ds), ('q', eh)):
            if c in bc.castle and (bz == cs or cm == cs or (p in 'Kk' and bz == (dz if c in 'KQ' else dy))):
                bc.castle = bc.castle.replace(c, '')
                bc.key ^= do[c]
        bc.side = 'b' if bc.side == 'w' else 'w'
        bc.key ^= dm
    def unmake(bc):
        bz, cm, p, cd, castle, ep, half, key = bc.hist.pop()
        b = bc.b
        b[bz] = p
        b[cm] = cd
        if p.lower() == 'p' and cm == ep and (cd == '.'):
            an = cm + (10 if p == 'P' else -10)
            b[an] = 'p' if p == 'P' else 'P'
        y = 'b' if bc.side == 'w' else 'w'
        if p in 'Kk' and abs(cm - bz) == 2:
            if cm == dv:
                b[dt], b[dx] = ('R', '.')
            elif cm == ed:
                b[ei], b[eb] = ('R', '.')
            elif cm == du:
                b[ds], b[dw] = ('r', '.')
            else:
                b[eh], b[ea] = ('r', '.')
        bc.castle, bc.ep, bc.half, bc.key = (castle, ep, half, key)
        bc.side = y
    def king_sq(bc, side):
        k = 'K' if side == 'w' else 'k'
        return bc.b.index(k) if k in bc.b else -1
    def in_check(bc, side=None):
        side = side or bc.side
        return ac(bc.b, bc.king_sq(side), side == 'b')
def ai(a, b):
    cx, dk = (a // 10, a % 10)
    cw, dj = (b // 10, b % 10)
    return cx == cw or dk == dj or abs(cx - cw) == abs(dk - dj)
def i(bs):
    bv = []
    aw = bs.side
    by = bs.king_sq(aw)
    bd = not bs.in_check(side=aw)
    for m in bs.moves():
        if m[3] == 2:
            bj = dz if m[1] in (dv, ed) else dy
            bx = (dx, dv) if m[1] == dv else (eb, ed) if m[1] == ed else (dw, du) if m[1] == du else (ea, ec)
            if any((ac(bs.b, s, aw == 'b') for s in (bj,) + bx)):
                continue
        if bd and bs.b[m[0]] not in 'Kk' and (m[3] != 1) and (not ai(m[0], by)):
            bv.append(m)
            continue
        bs.make(m)
        if not bs.in_check(side=aw):
            bv.append(m)
        bs.unmake()
    return bv
cj = {'p': (0, 0, 0, 0, 0, 0, 0, 0, 60, 60, 60, 60, 60, 60, 60, 60, 12, 18, 24, 30, 30, 24, 18, 12, 6, 10, 16, 26, 26, 16, 10, 6, 2, 4, 10, 22, 22, 10, 4, 2, 2, -2, -4, 4, 4, -4, -2, 2, 2, 4, 4, -8, -8, 4, 4, 2, 0, 0, 0, 0, 0, 0, 0, 0), 'n': (-40, -28, -18, -18, -18, -18, -28, -40, -24, -12, 0, 4, 4, 0, -12, -24, -14, 2, 10, 10, 10, 10, 2, -14, -10, 6, 14, 16, 16, 14, 6, -10, -10, 4, 14, 16, 16, 14, 4, -10, -16, 0, 10, 12, 12, 10, 0, -16, -26, -14, 0, 2, 2, 0, -14, -26, -46, -30, -20, -18, -18, -20, -30, -46), 'b': (-16, -8, -8, -8, -8, -8, -8, -16, -8, 2, 0, 0, 0, 0, 2, -8, -6, 4, 6, 8, 8, 6, 4, -6, -4, 6, 10, 12, 12, 10, 6, -4, -4, 8, 10, 12, 12, 10, 8, -4, -6, 10, 8, 8, 8, 8, 10, -6, -8, 10, 6, 4, 4, 6, 10, -8, -14, -8, -10, -8, -8, -10, -8, -14), 'r': (0, 0, 0, 0, 0, 0, 0, 0, 4, 8, 8, 8, 8, 8, 8, 4, -4, 0, 0, 0, 0, 0, 0, -4, -4, 0, 0, 0, 0, 0, 0, -4, -4, 0, 0, 0, 0, 0, 0, -4, -4, 0, 0, 0, 0, 0, 0, -4, -4, 0, 0, 0, 0, 0, 0, -4, 0, 0, 4, 8, 8, 4, 0, 0), 'k': (-50, -40, -30, -20, -20, -30, -40, -50, -36, -24, -12, 0, 0, -12, -24, -36, -26, -12, 10, 20, 20, 10, -12, -26, -16, 4, 18, 26, 26, 18, 4, -16, -8, 10, 22, 30, 30, 22, 10, -8, -4, 14, 26, 36, 36, 26, 14, -4, -4, 10, 16, 20, 20, 16, 10, -4, -10, -6, 0, 10, 10, 0, -6, -10)}
def ak(cs):
    r = cs // 10 - 2
    c = cs % 10 - 1
    return (r, c)
def aa(bs):
    b = bs.b
    ar = 0
    for cs in range(21, 99):
        p = b[cs]
        if p == ' ' or p == '.':
            continue
        dc = p.lower()
        r, c = ak(cs)
        v = cf[dc] + (cj[dc][r * 8 + c if p.isupper() else (7 - r) * 8 + c] if dc in cj else 0)
        if p.isupper():
            ar += v
        else:
            ar -= v
    return ar if bs.side == 'w' else -ar
bp = 100000
e = 50000
class bb(Exception):
    pass
def be(bs, moves, az, au, ao, ck, bf, ae):
    ba = -bp
    bo = None
    moves = [ae] + [m for m in moves if m != ae]
    for m in moves:
        ag = dict(bf)
        bs.make(m)
        ag[bs.key] = ag.get(bs.key, 0) + 1
        v = -ah(bs, az - 1, -bp, -ba, au, ao, ck, ag, 1)
        bs.unmake()
        if v > ba:
            ba = v
            bo = m
    return bo if bo else moves[0]
def ah(bs, az, ba, bn, au, ao, ck, bf, bt):
    au[0] += 1
    if au[0] > ao:
        raise bb()
    if bs.half >= 100:
        return 0
    am = bs.in_check()
    if am:
        az += 1
    if az <= 0:
        return af(bs, ba, bn, au, ao)
    key = bs.key
    ay = ck.get(key)
    ad = ay[3] if ay else None
    if not am and az >= 3:
        cq = (bs.side, bs.ep, bs.key)
        bs.side = 'b' if bs.side == 'w' else 'w'
        bs.key ^= dm ^ (ce[bs.ep] if bs.ep else 0)
        bs.ep = None
        da = -ah(bs, az - 3, -bn, -bn + 1, au, ao, ck, bf, bt + 1)
        bs.side, bs.ep, bs.key = cq
        if da >= bn:
            return da
    moves = i(bs)
    if not moves:
        return -bp + bt if am else 0
    if ay and ay[0] >= az:
        s, bk = (ay[1], ay[2])
        if bk == 0:
            return s
        if bk == 1 and s >= bn:
            return s
        if bk == 2 and s <= ba:
            return s
    def av(m):
        if ad and m == ad:
            return 1 << 30
        cd = bs.b[m[1]]
        if cd != '.':
            return (1 << 20) + cf[cd.lower()] * 10 - cf[bs.b[m[0]].lower()]
        if m[2]:
            return (1 << 20) - 1000
        df, co = (ak(m[0]), ak(m[1]))
        cn = cj.get(bs.b[m[0]].lower())
        if cn:
            return cn[co[0] * 8 + co[1]] - cn[df[0] * 8 + df[1]] if bs.side == 'w' else cn[(7 - co[0]) * 8 + co[1]] - cn[(7 - df[0]) * 8 + df[1]]
        return 0
    moves.sort(key=av, reverse=True)
    bo = -bp
    dl = ba
    for m in moves:
        ag = dict(bf)
        bs.make(m)
        ag[bs.key] = ag.get(bs.key, 0) + 1
        v = -ah(bs, az - 1, -bn, -ba, au, ao, ck, ag, bt + 1)
        bs.unmake()
        if v > bo:
            bo = v
            if v > ba:
                ba = v
        if ba >= bn:
            break
    bk = 0
    if bo <= dl:
        bk = 2
    elif bo >= bn:
        bk = 1
    ck[key] = (az, bo, bk, moves[0])
    return bo
def af(bs, ba, bn, au, ao, d=0):
    au[0] += 1
    if au[0] > ao:
        raise bb()
    if d > 8:
        return aa(bs)
    aq = aa(bs)
    if aq >= bn:
        return aq
    if aq + 950 < ba:
        return aq
    if aq > ba:
        ba = aq
    aw = bs.side
    for m in bs.moves(w=True):
        cd = bs.b[m[1]]
        if aq + cf[cd.lower() if cd != '.' else 'p'] + 200 <= ba:
            continue
        bs.make(m)
        if bs.in_check(side=aw):
            bs.unmake()
            continue
        v = -af(bs, -bn, -ba, au, ao, d + 1)
        bs.unmake()
        if v >= bn:
            return v
        if v > ba:
            ba = v
    return ba
def bq(m):
    f, t, at, bk = m
    de = lambda s: chr(97 + (s % 10 - 1)) + str(8 - (s // 10 - 2))
    return de(f) + de(t) + (at or '')
def main():
    g = bg('/game', {})
    while g.get('status') != 'done':
        if g.get('status') == 'your_move':
            bs = ci(g['fen'])
            ax = set(g['legal_moves'])
            ck = {}
            au = [0]
            moves = i(bs)
            moves = [m for m in moves if bq(m) in ax] or moves
            bo = moves[0] if moves else None
            if bo:
                for az in range(1, 64):
                    try:
                        bo = be(bs, moves, az, au, e, ck, bf, bo)
                    except bb:
                        break
                    moves = [bo] + [m for m in moves if m != bo]
                u = bq(bo)
            else:
                u = sorted(ax)[0]
            if u not in ax:
                u = min(ax)
            g = bg('/move', {'game': g['game'], 'move': u})
        else:
            g = bg('/game', {})
    sys.stderr.write(json.dumps({'wins': g.get('wins'), 'draws': g.get('draws'), 'losses': g.get('losses')}))
if __name__ == '__main__':
    main()