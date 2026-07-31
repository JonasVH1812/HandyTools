"""
mac_sorter.py
Author: jonasvh12

Sorts loose files and folders from Desktop, Downloads, and Documents
into Year/Month subfolders. Folders are moved as a whole, contents
are never touched. Dry run by default.
"""

from pathlib import Path
from datetime import datetime
import shutil
import re

HOME = Path.home()

ROOTS = [
    HOME / "Desktop",
    HOME / "Downloads",
    HOME / "Documents",
]

DRY_RUN = True

MONTHS = [
    "01-January", "02-February", "03-March", "04-April",
    "05-May", "06-June", "07-July", "08-August",
    "09-September", "10-October", "11-November", "12-December",
]

SKIP_EXTENSIONS = {".app"}
YEAR_PATTERN = re.compile(r"^\d{4}$")
MONTH_NAMES = set(MONTHS)


def is_protected_structure(item: Path) -> bool:
    if item.is_dir():
        if YEAR_PATTERN.match(item.name):
            return True
        if item.name in MONTH_NAMES:
            return True
    return False


def should_skip(item: Path) -> bool:
    if item.name.startswith("."):
        return True
    if item.is_symlink():
        return True
    if item.suffix.lower() in SKIP_EXTENSIONS:
        return True
    if is_protected_structure(item):
        return True
    return False


def get_item_date(item: Path) -> datetime:
    stat = item.stat()
    timestamp = getattr(stat, "st_birthtime", None) or stat.st_mtime
    return datetime.fromtimestamp(timestamp)


def gather_items(root: Path):
    if not root.exists():
        return []
    return [item for item in root.iterdir() if not should_skip(item)]


def sort_root(root: Path):
    items = gather_items(root)

    for item in items:
        try:
            created = get_item_date(item)
        except Exception as e:
            print(f"  [SKIP] Could not read date for {item.name}: {e}")
            continue

        year = str(created.year)
        month = MONTHS[created.month - 1]
        destination_dir = root / year / month
        destination_path = destination_dir / item.name

        if item.parent == destination_dir:
            continue

        if destination_path.exists():
            print(f"  [SKIP] {item.name} — already exists at {year}/{month}")
            continue

        kind = "folder" if item.is_dir() else "file"

        if DRY_RUN:
            print(f"  [DRY RUN] Would move {kind}: {item.name} -> {root.name}/{year}/{month}")
        else:
            try:
                destination_dir.mkdir(parents=True, exist_ok=True)
                shutil.move(str(item), str(destination_path))
                print(f"  Moved {kind}: {item.name} -> {root.name}/{year}/{month}")
            except Exception as e:
                print(f"  [ERROR] Could not move {item.name}: {e}")


def main():
    print("DRY RUN - nothing will actually move" if DRY_RUN else "LIVE RUN - files will be moved")
    print("=" * 60)

    for root in ROOTS:
        print(f"\nScanning: {root}")
        if not root.exists():
            print("  (folder does not exist, skipping)")
            continue
        sort_root(root)

    if DRY_RUN:
        print("\nThis was a dry run. Set DRY_RUN = False to actually move files.")


if __name__ == "__main__":
    main()