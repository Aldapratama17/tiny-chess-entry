# 4KB chess engine. Mailbox 10x12 board, negamax alpha-beta + TT + quiescence,
# fixed node budget (deterministic), PST + material eval.
import json, os, sys, urllib.request
from random import Random

ENV_URL = os.environ.get("MAKEFUN_ENV_URL") or sys.exit("MAKEFUN_ENV_URL is not set")

def post(path, body):
    req = urllib.request.Request(ENV_URL + path, data=json.dumps(body).encode(),
                                 headers={"content-type": "application/json"})
    return json.load(urllib.request.urlopen(req))

KN = (-21, -19, -12, -8, 8, 12, 19, 21)
KI = (-11, -10, -9, -1, 1, 9, 10, 11)
BI = (-11, -9, 9, 11)
RO = (-10, -1, 1, 10)
A1, B1, C1, D1, E1, F1, G1, H1 = 91, 92, 93, 94, 95, 96, 97, 98
A8, B8, C8, D8, E8, F8, G8, H8 = 21, 22, 23, 24, 25, 26, 27, 28

def parse_fen(fen):
    placement, side, castle, ep, half = fen.split()[:5]
    b = [' '] * 120
    for r in range(8):
        for c in range(8):
            b[21 + r * 10 + c] = '.'
    r = c = 0
    for ch in placement:
        if ch == '/':
            r += 1; c = 0
        elif ch.isdigit():
            c += int(ch)
        else:
            b[21 + r * 10 + c] = ch; c += 1
    ep = None if ep == '-' else 21 + (8 - int(ep[1])) * 10 + (ord(ep[0]) - 97)
    return b, side, castle, ep, int(half)

# --- zobrist ---
RNG = Random(12345)
PIECES = 'PNBRQKpnbrqk'
ZP = {p: [RNG.getrandbits(64) for _ in range(120)] for p in PIECES}
ZS = RNG.getrandbits(64)
ZC = {c: RNG.getrandbits(64) for c in 'KQkq'}
ZEP = {f: RNG.getrandbits(64) for f in range(120)}

def key_of(b, side, castle, ep):
    h = 0
    for sq in range(21, 99):
        p = b[sq]
        if p != ' ' and p != '.':
            h ^= ZP[p][sq]
    h ^= ZS if side == 'w' else 0
    for c in castle.replace('-', ''):
        h ^= ZC[c]
    if ep is not None:
        h ^= ZEP[ep]
    return h

def gen_moves(b, side, castle, ep, caps_only=False):
    """(frm,to,promo,flag) flag: 0 normal, 1 ep, 2 castle"""
    mv = []
    own = str.isupper if side == 'w' else str.islower
    for sq in range(21, 99):
        p = b[sq]
        if p == ' ' or p == '.' or not own(p):
            continue
        lo = p.lower()
        if lo == 'p':
            d = -10 if side == 'w' else 10
            promo_row = 2 if side == 'w' else 9
            one = sq + d
            if b[one] == '.' and not caps_only:
                if one // 10 == promo_row:
                    for pr in 'qrbn': mv.append((sq, one, pr, 0))
                else:
                    mv.append((sq, one, None, 0))
                    start_row = 8 if side == 'w' else 3
                    if sq // 10 == start_row and b[sq + 2 * d] == '.':
                        mv.append((sq, sq + 2 * d, None, 0))
            for dd in (d - 1, d + 1):
                t = sq + dd
                if b[t] == ' ': continue
                tp = b[t]
                if ep is not None and t == ep:
                    mv.append((sq, t, None, 1))
                elif tp != '.' and not own(tp):
                    if t // 10 == promo_row:
                        for pr in 'qrbn': mv.append((sq, t, pr, 0))
                    else:
                        mv.append((sq, t, None, 0))
        elif lo == 'n':
            for d in KN:
                t = sq + d
                tp = b[t]
                if tp == ' ': continue
                if tp == '.':
                    if not caps_only: mv.append((sq, t, None, 0))
                elif not own(tp):
                    mv.append((sq, t, None, 0))
        elif lo == 'k':
            for d in KI:
                t = sq + d
                tp = b[t]
                if tp == ' ': continue
                if tp == '.':
                    if not caps_only: mv.append((sq, t, None, 0))
                elif not own(tp):
                    mv.append((sq, t, None, 0))
            if not caps_only:
                if side == 'w':
                    if 'K' in castle and b[F1] == '.' and b[G1] == '.' and b[E1] == 'K' and b[H1] == 'R':
                        mv.append((E1, G1, None, 2))
                    if 'Q' in castle and b[D1] == '.' and b[C1] == '.' and b[B1] == '.' and b[E1] == 'K' and b[A1] == 'R':
                        mv.append((E1, C1, None, 2))
                else:
                    if 'k' in castle and b[F8] == '.' and b[G8] == '.' and b[E8] == 'k' and b[H8] == 'r':
                        mv.append((E8, G8, None, 2))
                    if 'q' in castle and b[D8] == '.' and b[C8] == '.' and b[B8] == '.' and b[E8] == 'k' and b[A8] == 'r':
                        mv.append((E8, C8, None, 2))
        else:
            dirs = BI if lo == 'b' else RO if lo == 'r' else KI
            for d in dirs:
                t = sq + d
                while b[t] != ' ':
                    tp = b[t]
                    if tp == '.':
                        if not caps_only: mv.append((sq, t, None, 0))
                    elif not own(tp):
                        mv.append((sq, t, None, 0)); break
                    else:
                        break
                    t += d
    return mv

VAL = dict(zip('pnbrqk', (100, 320, 330, 500, 900, 0)))

def attacked(b, sq, by_white):
    """is sq attacked by the given colour?"""
    lo = 'pnbrqk' if by_white else 'PNBRQK'
    for d in KN:
        if b[sq + d] == ('N' if by_white else 'n'): return True
    for d in KI:
        if b[sq + d] == ('K' if by_white else 'k'): return True
    pd = 10 if by_white else -10
    for d in (pd - 1, pd + 1):
        if b[sq + d] == ('P' if by_white else 'p'): return True
    for d in BI:
        t = sq + d
        while b[t] != ' ':
            p = b[t]
            if p != '.':
                if p in ('B', 'b') or p in ('Q', 'q'):
                    if (p.isupper()) == by_white: return True
                break
            t += d
    for d in RO:
        t = sq + d
        while b[t] != ' ':
            p = b[t]
            if p != '.':
                if p in ('R', 'r') or p in ('Q', 'q'):
                    if (p.isupper()) == by_white: return True
                break
            t += d
    return False

# --- make/unmake ---
class Pos:
    __slots__ = ('b','side','castle','ep','half','key','hist')

    def __init__(self, fen):
        self.b, self.side, self.castle, self.ep, self.half = parse_fen(fen)
        self.key = key_of(self.b, self.side, self.castle, self.ep)
        self.hist = []

    def moves(self, caps_only=False):
        return gen_moves(self.b, self.side, self.castle, self.ep, caps_only)

    def make(self, m):
        frm, to, promo, flag = m
        b = self.b
        p = b[frm]
        cap = b[to]
        st = (frm, to, p, cap, self.castle, self.ep, self.half, self.key)
        self.hist.append(st)
        self.key ^= ZP[p][frm] ^ ZS
        if cap != '.':
            self.key ^= ZP[cap][to]
        newp = (promo.upper() if self.side == 'w' else promo) if promo else p
        b[to] = newp
        b[frm] = '.'
        self.key ^= ZP[newp][to]
        self.ep = None
        half_inc = 1
        if p.lower() == 'p' or cap != '.':
            half_inc = 0
        self.half = self.half + half_inc
        if flag == 1:  # en passant capture
            cap_sq = to + (10 if self.side == 'w' else -10)
            cp = b[cap_sq]
            self.key ^= ZP[cp][cap_sq]
            b[cap_sq] = '.'
        elif flag == 2:  # castle: move the rook
            if to == G1: rf, rt, rp = H1, F1, 'R'
            elif to == C1: rf, rt, rp = A1, D1, 'R'
            elif to == G8: rf, rt, rp = H8, F8, 'r'
            else: rf, rt, rp = A8, D8, 'r'
            b[rf] = '.'; b[rt] = rp
            self.key ^= ZP[rp][rf] ^ ZP[rp][rt]
        elif p.lower() == 'p' and abs(to - frm) == 20:
            self.ep = (frm + to) // 2
            self.key ^= ZEP[self.ep]
        # castling rights
        for c, sq in (('K', H1), ('Q', A1), ('k', H8), ('q', A8)):
            if c in self.castle and (frm == sq or to == sq or (p in 'Kk' and frm == (E1 if c in 'KQ' else E8))):
                self.castle = self.castle.replace(c, '')
                self.key ^= ZC[c]
        self.side = 'b' if self.side == 'w' else 'w'
        self.key ^= ZS

    def unmake(self):
        frm, to, p, cap, castle, ep, half, key = self.hist.pop()
        b = self.b
        b[frm] = p
        b[to] = cap
        if p.lower() == 'p' and to == ep and cap == '.':
            cap_sq = to + (10 if p == 'P' else -10)
            b[cap_sq] = 'p' if p == 'P' else 'P'
        side_now = 'b' if self.side == 'w' else 'w'  # mover's side
        if p in 'Kk' and abs(to - frm) == 2:
            if to == G1: b[H1], b[F1] = 'R', '.'
            elif to == C1: b[A1], b[D1] = 'R', '.'
            elif to == G8: b[H8], b[F8] = 'r', '.'
            else: b[A8], b[D8] = 'r', '.'
        self.castle, self.ep, self.half, self.key = castle, ep, half, key
        self.side = side_now

    def king_sq(self, side):
        k = 'K' if side == 'w' else 'k'
        return self.b.index(k) if k in self.b else -1

    def in_check(self, side=None):
        side = side or self.side
        return attacked(self.b, self.king_sq(side), side == 'b')

def aligned(a, b):
    ra, ca = a // 10, a % 10
    rb, cb = b // 10, b % 10
    return ra == rb or ca == cb or abs(ra - rb) == abs(ca - cb)

def legal_moves(pos):
    out = []
    mover = pos.side
    ksq = pos.king_sq(mover)
    safe = not pos.in_check(side=mover)
    for m in pos.moves():
        if m[3] == 2:  # castle: from, transit and to must not be attacked
            home = E1 if m[1] in (G1, C1) else E8
            mid = (F1, G1) if m[1] == G1 else (D1, C1) if m[1] == C1 else (F8, G8) if m[1] == G8 else (D8, C8)
            if any(attacked(pos.b, s, mover == 'b') for s in (home,) + mid):
                continue
        if safe and pos.b[m[0]] not in 'Kk' and m[3] != 1 and not aligned(m[0], ksq):
            out.append(m)  # cannot expose the king
            continue
        pos.make(m)
        if not pos.in_check(side=mover):
            out.append(m)
        pos.unmake()
    return out

def perft(pos, d):
    if d == 0: return 1
    n = 0
    for m in legal_moves(pos):
        pos.make(m)
        n += perft(pos, d - 1)
        pos.unmake()
    return n

# --- evaluation: material + my own piece-square tables (white view, a8=h1 rows) ---
PST = {
 'p': (0,0,0,0,0,0,0,0,
       60,60,60,60,60,60,60,60,
       12,18,24,30,30,24,18,12,
       6,10,16,26,26,16,10,6,
       2,4,10,22,22,10,4,2,
       2,-2,-4,4,4,-4,-2,2,
       2,4,4,-8,-8,4,4,2,
       0,0,0,0,0,0,0,0),
 'n': (-40,-28,-18,-18,-18,-18,-28,-40,
       -24,-12,0,4,4,0,-12,-24,
       -14,2,10,10,10,10,2,-14,
       -10,6,14,16,16,14,6,-10,
       -10,4,14,16,16,14,4,-10,
       -16,0,10,12,12,10,0,-16,
       -26,-14,0,2,2,0,-14,-26,
       -46,-30,-20,-18,-18,-20,-30,-46),
 'b': (-16,-8,-8,-8,-8,-8,-8,-16,
       -8,2,0,0,0,0,2,-8,
       -6,4,6,8,8,6,4,-6,
       -4,6,10,12,12,10,6,-4,
       -4,8,10,12,12,10,8,-4,
       -6,10,8,8,8,8,10,-6,
       -8,10,6,4,4,6,10,-8,
       -14,-8,-10,-8,-8,-10,-8,-14),
 'r': (0,0,0,0,0,0,0,0,
       4,8,8,8,8,8,8,4,
       -4,0,0,0,0,0,0,-4,
       -4,0,0,0,0,0,0,-4,
       -4,0,0,0,0,0,0,-4,
       -4,0,0,0,0,0,0,-4,
       -4,0,0,0,0,0,0,-4,
       0,0,4,8,8,4,0,0),
 'k': (-50,-40,-30,-20,-20,-30,-40,-50,
       -36,-24,-12,0,0,-12,-24,-36,
       -26,-12,10,20,20,10,-12,-26,
       -16,4,18,26,26,18,4,-16,
       -8,10,22,30,30,22,10,-8,
       -4,14,26,36,36,26,14,-4,
       -4,10,16,20,20,16,10,-4,
       -10,-6,0,10,10,0,-6,-10),
}
def sq_idx(sq):
    """convert mailbox sq to (row over 8x8 from rank8), file"""
    r = sq // 10 - 2
    c = sq % 10 - 1
    return r, c

def evaluate(pos):
    """from white's view."""
    b = pos.b
    score = 0
    for sq in range(21, 99):
        p = b[sq]
        if p == ' ' or p == '.':
            continue
        lo = p.lower()
        r, c = sq_idx(sq)
        v = VAL[lo] + (PST[lo][(r * 8 + c) if p.isupper() else ((7 - r) * 8 + c)] if lo in PST else 0)
        if p.isupper():
            score += v
        else:
            score -= v
    return score if pos.side == 'w' else -score

MATE = 100000
NODES_BUDGET = 50000

class Abort(Exception):
    pass

def search_root(pos, budget=NODES_BUDGET):
    """iterative deepening with a node cap; returns the best move."""
    tt = {}
    nodes = [0]
    reps = {pos.key: 1}
    moves = legal_moves(pos)
    if not moves:
        return None
    best = moves[0]
    for depth in range(1, 64):
        try:
            best = root(pos, moves, depth, nodes, budget, tt, reps, best)
        except Abort:
            break
        moves = [best] + [m for m in moves if m != best]
    return best

def root(pos, moves, depth, nodes, budget, tt, reps, tt_best):
    alpha = -MATE
    best = None
    moves = [tt_best] + [m for m in moves if m != tt_best]
    for m in moves:
        newreps = dict(reps)
        pos.make(m)
        newreps[pos.key] = newreps.get(pos.key, 0) + 1
        v = -negamax(pos, depth - 1, -MATE, -alpha, nodes, budget, tt, newreps, 1)
        pos.unmake()
        if v > alpha:
            alpha = v
            best = m
    return best if best else moves[0]

def negamax(pos, depth, alpha, beta, nodes, budget, tt, reps, ply):
    nodes[0] += 1
    if nodes[0] > budget:
        raise Abort()
    if pos.half >= 100:
        return 0
    in_chk = pos.in_check()
    if in_chk:
        depth += 1
    if depth <= 0:
        return quiesce(pos, alpha, beta, nodes, budget)
    key = pos.key
    entry = tt.get(key)
    tt_move = entry[3] if entry else None
    if not in_chk and depth >= 3:
        sv = (pos.side, pos.ep, pos.key)
        pos.side = 'b' if pos.side == 'w' else 'w'
        pos.key ^= ZS ^ (ZEP[pos.ep] if pos.ep else 0)
        pos.ep = None
        nv = -negamax(pos, depth - 3, -beta, -beta + 1, nodes, budget, tt, reps, ply + 1)
        pos.side, pos.ep, pos.key = sv
        if nv >= beta:
            return nv
    moves = legal_moves(pos)
    if not moves:
        return -MATE + ply if in_chk else 0
    if entry and entry[0] >= depth:
        s, flag = entry[1], entry[2]
        if flag == 0:
            return s
        if flag == 1 and s >= beta:
            return s
        if flag == 2 and s <= alpha:
            return s
    def mrank(m):
        if tt_move and m == tt_move:
            return 1 << 30
        cap = pos.b[m[1]]
        if cap != '.':
            return (1 << 20) + VAL[cap.lower()] * 10 - VAL[pos.b[m[0]].lower()]
        if m[2]:
            return (1 << 20) - 1000
        f0, t0 = sq_idx(m[0]), sq_idx(m[1])
        tb = PST.get(pos.b[m[0]].lower())
        if tb:
            return (tb[t0[0] * 8 + t0[1]] - tb[f0[0] * 8 + f0[1]]) if pos.side == 'w' else (tb[(7 - t0[0]) * 8 + t0[1]] - tb[(7 - f0[0]) * 8 + f0[1]])
        return 0
    moves.sort(key=mrank, reverse=True)
    best = -MATE
    a0 = alpha
    for m in moves:
        newreps = dict(reps)
        pos.make(m)
        newreps[pos.key] = newreps.get(pos.key, 0) + 1
        v = -negamax(pos, depth - 1, -beta, -alpha, nodes, budget, tt, newreps, ply + 1)
        pos.unmake()
        if v > best:
            best = v
            if v > alpha:
                alpha = v
        if alpha >= beta:
            break
    flag = 0
    if best <= a0:
        flag = 2
    elif best >= beta:
        flag = 1
    tt[key] = (depth, best, flag, moves[0])
    return best

def quiesce(pos, alpha, beta, nodes, budget, d=0):
    nodes[0] += 1
    if nodes[0] > budget:
        raise Abort()
    if d > 8:
        return evaluate(pos)
    stand = evaluate(pos)
    if stand >= beta:
        return stand
    if stand + 950 < alpha:
        return stand
    if stand > alpha:
        alpha = stand
    mover = pos.side
    for m in pos.moves(caps_only=True):
        cap = pos.b[m[1]]
        if stand + VAL[cap.lower() if cap != '.' else 'p'] + 200 <= alpha:
            continue
        pos.make(m)
        if pos.in_check(side=mover):
            pos.unmake()
            continue
        v = -quiesce(pos, -beta, -alpha, nodes, budget, d + 1)
        pos.unmake()
        if v >= beta:
            return v
        if v > alpha:
            alpha = v
    return alpha

def uci(m):
    f, t, promo, flag = m
    fs = lambda s: chr(97 + (s % 10 - 1)) + str(8 - (s // 10 - 2))
    return fs(f) + fs(t) + (promo or '')

def main():
    g = post('/game', {})
    while g.get('status') != 'done':
        if g.get('status') == 'your_move':
            pos = Pos(g['fen'])
            legal = set(g['legal_moves'])
            tt = {}
            nodes = [0]
            moves = legal_moves(pos)
            moves = [m for m in moves if uci(m) in legal] or moves
            best = moves[0] if moves else None
            if best:
                for depth in range(1, 64):
                    try:
                        best = root(pos, moves, depth, nodes, NODES_BUDGET, tt, reps, best)
                    except Abort:
                        break
                    moves = [best] + [m for m in moves if m != best]
                u = uci(best)
            else:
                u = sorted(legal)[0]
            if u not in legal:
                u = min(legal)
            g = post('/move', {'game': g['game'], 'move': u})
        else:
            g = post('/game', {})
    sys.stderr.write(json.dumps({'wins': g.get('wins'), 'draws': g.get('draws'), 'losses': g.get('losses')}))

if __name__ == '__main__':
    main()
