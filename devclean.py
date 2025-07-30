import os
import shutil
import argparse
from pathlib import Path
from colorama import init, Fore, Style

init(autoreset=True)

# Common folders safe to delete
DELETE_KEYWORDS = {
    "node_modules", "build", "dist", ".next", ".turbo", ".cache", ".pytest_cache",
    "coverage", ".parcel-cache", ".eslintcache", ".vite", ".angular", "out",
    ".serverless", ".vercel", ".netlify", ".svelte-kit", "tmp", "temp", "target",
    "__pycache__", ".trash", ".DS_Store"
}

# Do not touch these folders
PROTECTED_DIRS = {'.git', '.github', '.idea', '.vscode'}

def should_delete(dirname):
    """Check if folder matches known deletable keywords"""
    name = dirname.lower()
    return any(kw in name for kw in DELETE_KEYWORDS)

def get_folder_size(path):
    """Calculate folder size in bytes (recursive)"""
    total = 0
    for dirpath, _, filenames in os.walk(path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            if os.path.exists(fp):
                try:
                    total += os.path.getsize(fp)
                except OSError:
                    pass
    return total

def human_readable_size(size_bytes):
    """Convert byte count to human-readable form"""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_bytes < 1024:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024

def delete_deletable_dirs(base_path, dry_run=False, silent=False, log_path=None, force=False, show_size=False):
    deleted = []
    skipped = []
    total_size_bytes = 0

    for root, dirs, _ in os.walk(base_path, topdown=False):
        for d in dirs:
            full_path = os.path.join(root, d)
            if d in PROTECTED_DIRS:
                skipped.append(full_path)
                continue

            if should_delete(d):
                folder_size = get_folder_size(full_path) if show_size else 0
                if show_size:
                    total_size_bytes += folder_size

                if dry_run:
                    if not silent:
                        size_info = f" ({human_readable_size(folder_size)})" if show_size else ""
                        print(Fore.YELLOW + f"[DRY RUN] Would delete: {full_path}{size_info}")
                    deleted.append(full_path)
                else:
                    if not force:
                        confirm = input(f"❓ Confirm delete {full_path}? (y/n): ").strip().lower()
                        if confirm != 'y':
                            skipped.append(full_path)
                            continue
                    try:
                        shutil.rmtree(full_path)
                        if not silent:
                            size_info = f" ({human_readable_size(folder_size)})" if show_size else ""
                            print(Fore.GREEN + f"✅ Deleted: {full_path}{size_info}")
                        deleted.append(full_path)
                    except Exception as e:
                        print(Fore.RED + f"❌ Error deleting {full_path}: {e}")

    # Summary
    if dry_run:
        print(Fore.CYAN + f"\n👀 Dry run complete. {len(deleted)} folder(s) would be deleted.")
    else:
        print(Fore.GREEN + f"\n🧹 Cleanup complete. Deleted {len(deleted)} folder(s).")

    if show_size:
        print(Fore.MAGENTA + f"💾 Total space {'to be freed' if dry_run else 'freed'}: {human_readable_size(total_size_bytes)}")

    if skipped and not silent:
        print(Fore.LIGHTBLACK_EX + f"\n⏭️ Skipped {len(skipped)} protected folder(s).")

    if log_path:
        with open(log_path, 'w') as log_file:
            for path in deleted:
                log_file.write(f"Deleted: {path}\n")
            for path in skipped:
                log_file.write(f"Skipped: {path}\n")
            if show_size:
                log_file.write(f"\nTotal size {'to be freed' if dry_run else 'freed'}: {human_readable_size(total_size_bytes)}\n")
        print(Fore.BLUE + f"\n📝 Log written to: {log_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Clean dev/temp folders like node_modules, build, dist, etc.")
    parser.add_argument("--path", "-p", type=str, default=".", help="Root path to scan (default: current directory)")
    parser.add_argument("--dry-run", "-d", action="store_true", help="Preview what would be deleted")
    parser.add_argument("--silent", "-s", action="store_true", help="Suppress detailed output")
    parser.add_argument("--log", "-l", type=str, help="Write deleted/skipped paths and size to a log file")
    parser.add_argument("--force", "-f", action="store_true", help="Delete without asking for confirmation")
    parser.add_argument("--show-size", "-z", action="store_true", help="Also calculate and show folder sizes")

    args = parser.parse_args()
    path = args.path

    if not os.path.exists(path):
        print(Fore.RED + "❌ Provided path does not exist.")
    else:
        delete_deletable_dirs(
            base_path=path,
            dry_run=args.dry_run,
            silent=args.silent,
            log_path=args.log,
            force=args.force,
            show_size=args.show_size
        )
