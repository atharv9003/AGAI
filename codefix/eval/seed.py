"""Seed runs baked into the container image, so a cold instance is never a blank demo.

Cloud Run gives each instance a fresh `/tmp`, and that is where `runs.db` and the traces live
(`CODEFIX_DATA_DIR`). A cold start therefore shows an empty Runs list and an empty Dashboard —
fine for a service, bad in front of an examiner.

`export_seed` snapshots a chosen set of finished runs (every row that references them, plus
their JSONL traces) into `benchmarks/seed/`, which the Dockerfile already copies into the image.
`restore_seed` copies that into the data directory on startup *only when no database exists
yet*, so it can never overwrite real runs — including the ones made during the demo itself.
"""

from __future__ import annotations

import shutil
import sqlite3
from pathlib import Path

from codefix import config

SEED_DIR = config.ROOT / "benchmarks" / "seed"
TABLES = ("runs", "artifacts", "messages", "llm_calls", "tool_calls", "evaluations")


def export_seed(task_ids: list[str], out_dir: Path | None = None, src_db: Path | None = None) -> dict:
    """Copy `task_ids` and everything referencing them from runs.db into a seed directory."""
    out = Path(out_dir or SEED_DIR)
    src = Path(src_db or config.DB_PATH)
    if not src.exists():
        raise FileNotFoundError(f"no database at {src}")
    if not task_ids:
        raise ValueError("refusing to build an empty seed")
    out.mkdir(parents=True, exist_ok=True)
    (out / "traces").mkdir(exist_ok=True)
    db = out / "runs.db"
    db.unlink(missing_ok=True)

    from codefix.blackboard.store import Blackboard

    Blackboard(db, out / "traces")  # create the schema (+ additive migrations) in the seed file
    counts: dict[str, int] = {}
    s, d = sqlite3.connect(src), sqlite3.connect(db)
    try:
        s.row_factory = sqlite3.Row
        marks = ",".join("?" * len(task_ids))
        for table in TABLES:
            rows = s.execute(f"SELECT * FROM {table} WHERE task_id IN ({marks})", task_ids).fetchall()
            if not rows:
                counts[table] = 0
                continue
            # only columns the seed schema also has, so an older source db still exports cleanly
            keep = [c for c in rows[0].keys()
                    if c in {r[1] for r in d.execute(f"PRAGMA table_info({table})")}]
            d.executemany(
                f"INSERT OR REPLACE INTO {table} ({','.join(keep)}) VALUES ({','.join('?' * len(keep))})",
                [tuple(r[c] for c in keep) for r in rows],
            )
            counts[table] = len(rows)
        d.commit()
        # The Blackboard runs in WAL mode, so these rows are still in runs.db-wal. The seed ships
        # as a single file copied with shutil, so fold the WAL back into the main database —
        # otherwise the seed arrives empty on the deployed instance.
        d.execute("PRAGMA wal_checkpoint(TRUNCATE)")
    finally:
        s.close()
        d.close()
    for stale in (db.with_name(db.name + "-wal"), db.with_name(db.name + "-shm")):
        stale.unlink(missing_ok=True)

    traces = 0
    for tid in task_ids:
        for f in config.TRACES_DIR.glob(f"{tid}*"):
            shutil.copy2(f, out / "traces" / f.name)
            traces += 1
    counts["traces"] = traces
    return counts


def restore_seed(data_dir: Path | None = None, seed_dir: Path | None = None) -> bool:
    """Install the seed into the data directory if it has no database yet. Returns True if it did."""
    data = Path(data_dir or config.DATA_DIR)
    seed = Path(seed_dir or SEED_DIR)
    db = data / "runs.db"
    if db.exists() or not (seed / "runs.db").exists():
        return False
    data.mkdir(parents=True, exist_ok=True)
    shutil.copy2(seed / "runs.db", db)
    if (seed / "traces").is_dir():
        dest = data / "traces"
        dest.mkdir(parents=True, exist_ok=True)
        for f in (seed / "traces").iterdir():
            if f.is_file():
                shutil.copy2(f, dest / f.name)
    return True


def pick_demo_runs(limit: int = 12, src_db: Path | None = None) -> list[str]:
    """A representative spread for the dashboard: prefer variety of architecture and outcome,
    and make sure a retried run is included — the retry loop is the point of the system."""
    src = Path(src_db or config.DB_PATH)
    with sqlite3.connect(src) as c:
        c.row_factory = sqlite3.Row
        rows = c.execute(
            "SELECT task_id, arch, outcome, attempts FROM runs "
            "WHERE llm_mode != 'mock' AND outcome IS NOT NULL ORDER BY created_at DESC"
        ).fetchall()
    picked: list[str] = []
    seen: set[tuple] = set()
    for want_retry in (True, False):          # one pass for retried runs, then fill
        for r in rows:
            if len(picked) >= limit:
                break
            if (r["attempts"] or 1) > 1 and not want_retry:
                continue
            if want_retry and (r["attempts"] or 1) <= 1:
                continue
            key = (r["arch"], r["outcome"], (r["attempts"] or 1) > 1)
            if key in seen and len(picked) > 3:
                continue
            seen.add(key)
            picked.append(r["task_id"])
    return picked[:limit]
