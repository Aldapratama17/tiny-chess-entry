# tiny-chess-01 entry — MTD-bi chess engine

A chess engine for the make.fun [tiny-chess-01 bounty](https://make.fun/bounty/tiny-chess-01),
written in at most 4,096 bytes of Python (packed `main.py`).

## What it does

`main.py` is an lzma-packed entry whose readable source is `sf_engine.py`:
a 120-square mailbox board, an MTD-bi transposition-table search with late-move
reduction, quiescence search and piece-square-table evaluation, playing the
make.fun env protocol (`MAKEFUN_ENV_URL`), fixed at 50,000 nodes per move for
determinism.

## Credits

The search and evaluation are adapted from
[sunfish](https://github.com/thomasahle/sunfish) by Thomas Ahle and
contributors (`nnue_4k/pst_entry.py`, commit e396948, GPL-3.0-only), with the
env driver rewritten for this competition. This entry is therefore licensed
GPL-3.0-only.

## Run

```sh
MAKEFUN_ENV_URL=http://127.0.0.1:8099 python3 main.py
```

against the kit's practice env server (`node program/env/server.mjs`).
