import hashlib
import os
import json

MONITOR_DIR = "monitored_files"
BASELINE_FILE = "baseline_hashes.json"


def calculate_hash(file_path):
    sha256 = hashlib.sha256()
    with open(file_path, "rb") as f:
        while True:
            data = f.read(4096)
            if not data:
                break
            sha256.update(data)
    return sha256.hexdigest()


def create_baseline():
    # Create folder if missing
    if not os.path.exists(MONITOR_DIR):
        os.makedirs(MONITOR_DIR)
        print(f"'{MONITOR_DIR}' folder created.")
        print("Add files inside it and run again.\n")
        return

    files = os.listdir(MONITOR_DIR)
    if not files:
        print("No files found in monitored_files folder.")
        print("Add files and run again.\n")
        return

    hashes = {}
    for file in files:
        path = os.path.join(MONITOR_DIR, file)
        if os.path.isfile(path):
            hashes[file] = calculate_hash(path)

    with open(BASELINE_FILE, "w") as f:
        json.dump(hashes, f, indent=4)

    print("✅ Baseline created successfully!\n")


def check_integrity():
    # If baseline missing → create it automatically
    if not os.path.exists(BASELINE_FILE):
        print("Baseline not found. Creating baseline first...\n")
        create_baseline()
        return

    with open(BASELINE_FILE, "r") as f:
        baseline = json.load(f)

    print("🔍 Checking File Integrity...\n")

    for file, old_hash in baseline.items():
        path = os.path.join(MONITOR_DIR, file)

        if not os.path.exists(path):
            print(f"[ALERT] {file} was DELETED!")
            continue

        new_hash = calculate_hash(path)
        if new_hash != old_hash:
            print(f"[WARNING] {file} was MODIFIED!")
        else:
            print(f"[OK] {file} is unchanged.")

    print()


if __name__ == "__main__":
    print("1. Create Baseline")
    print("2. Check Integrity")

    choice = input("Enter your choice (1/2): ")

    if choice == "1":
        create_baseline()
    elif choice == "2":
        check_integrity()
    else:
        print("Invalid choice")