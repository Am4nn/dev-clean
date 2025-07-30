# 🧹 clean-dev-folders

A simple, safe, and powerful Python CLI tool to clean up development clutter like `node_modules`, `dist`, `build`, `.cache`, etc.

## 🚀 Features

- 🔍 **Smart Detection**  
  Automatically finds and targets common development and temp folders such as:
  `node_modules`, `dist`, `build`, `.next`, `__pycache__`, and more.

- 🧪 **Dry-Run Mode**  
  Use `--dry-run` to preview what will be deleted — no changes are made to your system.

- 🛡️ **Safe by Default**  
  - Skips protected folders like `.git`, `.github`, `.idea`, `.vscode`
  - Asks for confirmation before deletion (unless `--force` is used)

- 💾 **Optional Folder Size Estimation**  
  Use `--show-size` to display how much disk space would be or was freed.

- 📝 **Logging Support**  
  Generate detailed logs with `--log out.txt` including deleted paths, skipped folders, and size info.

- 🤫 **Silent or Interactive**  
  - `--force` skips confirmation prompts  
  - `--silent` suppresses all intermediate logs (great for scripting)

- ⚙️ **CLI Control & Scripting**  
  Fine-tuned control using CLI flags:  
  `--path`, `--dry-run`, `--silent`, `--log`, `--force`, `--show-size`

- ✅ **Cross-Platform & Easy to Use**  
  Works on **Windows, macOS, and Linux** — just install Python and run the script.

## 🛠️ Usage

### 📦 Installation

Install dependencies:

```bash
pip install colorama
```

### 🔧 Run the script

```bash
python clean_dev_folders.py [options]
```

### 💡 Examples

| Command | Description |
|----------|----------|
| `python devclean.py -p ./ -d` | Dry run without size (fast) |
| `python devclean.py -d -z` | Dry run with size info |
| `python devclean.py -f --show-size` | Force delete + show how much space was freed |
| `python devclean.py -f -l deleted.log` | Force delete and log actions |
| `python devclean.py -p ./ -f -z -l deleted.log` | Everything enabled |

### 🔧 My Personal Workflow

Start by running a **dry run** with `--show-size` to preview what will be deleted and how much space will be freed:

```bash
python devclean.py --path "/your/dir" --dry-run --show-size --silent --log ./out.txt
```

Then, perform the actual cleanup using the `--force` flag to delete without confirmation prompts:

```bash
python devclean.py --path "/your/dir" --force --show-size --silent --log ./out.txt
```

Finally, re-run the dry run to confirm everything is cleaned up — it should report 0 bytes to delete.

You can use `devclean-dryrun.sh` and `devclean-clean.sh` to run both the commands.

⚠️ Note: `--show-size` can slow things down on large directories. Use it based on your needs.

## 🧰 Options

| Option | Description |
|----------|----------|
| `--path`, `-p` | Root path to clean (default: current directory) |
| `--dry-run`, `-d` | Preview what would be deleted |
| `--silent`, `-s` | Suppress output except summary |
| `--log`, `-l` | Write deleted/skipped paths to log file |
| `--force`, `-f` | Delete without asking for confirmation |
| `--show-size`, `-z` | Print total space that will be freed on deletion |

## 📄 License

MIT License
