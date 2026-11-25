"""Standalone script to initialize the SQLite database and seed synthetic papers."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

BACKEND_DIR = Path(__file__).resolve().parents[1]
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

from app.database import Base, SessionLocal, engine
from app.utils.dataset_loader import seed_papers_if_empty


def main() -> None:
    parser = argparse.ArgumentParser(description="Seed ResearchLens SQLite database.")
    parser.add_argument("--force", action="store_true", help="Re-seed all papers from dataset files.")
    args = parser.parse_args()

    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        total = seed_papers_if_empty(db, force=args.force)
        print(f"Database initialized. Total papers in SQLite: {total}")
    finally:
        db.close()


if __name__ == "__main__":
    main()
