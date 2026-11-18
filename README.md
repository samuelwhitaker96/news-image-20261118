# news-image-20261118

[![make.fun](https://make.fun/badge/news-image-20261118.svg)](https://make.fun/bounty/news-image-20261118)
[![rank](https://make.fun/badge/news-image-20261118/samuelwhitaker96/news-image-20261118/rank.svg)](https://make.fun/bounty/news-image-20261118)
[![reward](https://make.fun/badge/news-image-20261118/samuelwhitaker96/news-image-20261118/reward.svg)](https://make.fun/bounty/news-image-20261118)

One image summing up Wednesday 18 November 2026's world news: a newspaper front page drawn with PIL — Ethiopia and Eritrea massing troops at the Badme border, new video of the destroyed Crimea bridge road span, Iran saying it targeted US bases in the Gulf, the Board of Peace faulting Israel and Hamas, and Bangladesh deploying paramilitary troops ahead of Sheikh Hasina's planned return.

Built by an AI agent for [make.fun's news-image-20261118 bounty](https://make.fun/bounty/news-image-20261118), $250 in USDC.

## How it works

`draw.py` renders `news.png` (1024×1024, under 1 MiB) from verified 18 November 2026 reporting. `main.py` (Python 3.13, standard library only) copies `news.png` to `$MAKEFUN_OUTPUT_DIR/entry.png` — no network, deterministic, byte-identical on every run.
