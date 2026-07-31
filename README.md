# Handy Tools

A small collection of quality-of-life scripts for your computer.

## Contents

- `computerCleanUpBeta.py` — Mac cleanup script

## mac_sorter.py

Sorts loose files and folders from your Desktop, Downloads, and Documents into a clean `Year/Month` structure. Folders get moved as a whole, so nothing inside them gets touched or reorganized. <mark>Important: in the file there is a variable named DRY_RUN, this is set to true so you can see what it is going to do without doing it. Change it to false to make it actually move files. this is explained more in usage.</mark>

**Setup**

Mac only. On modern macOS you'll need to grant your terminal (or VS Code) access to these folders:

`System Settings → Privacy & Security → Files and Folders`

**usage**

By default the script runs in dry-run mode, printing what it would move without touching anything.

```bash
python3 mac_sorter.py
```

Once you're happy with the output, open the script, set `DRY_RUN = False`, and run it again to actually move things.

## preview Screenshots

### before
![Before](images/before.png)

### after
![After](images/after.png)
