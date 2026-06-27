import sys

# `python -m motif` runs the full Motif platform CLI (same surface as `motif`, `ii`,
# `oii`). The foundation-only CLI remains importable as `motif.cli`.
from ii.cli import main

if __name__ == "__main__":
    sys.exit(main())
