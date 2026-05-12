import sys
from forensic_core import update_field

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python update_main.py <batch_json>")
    else:
        update_field(sys.argv[1], "main-translation")
