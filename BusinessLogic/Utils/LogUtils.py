import sys

def log_info(message):
    print(f"[INFO] {message}", file=sys.stdout)

def log_warning(message):
    print(f"[WARN] {message}", file=sys.stdout)

def log_error(message):
    print(f"[ERROR] {message}", file=sys.stderr)
