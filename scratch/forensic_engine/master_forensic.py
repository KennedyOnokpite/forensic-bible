import os
import sys
import subprocess

def run_all(batch_dir):
    fields = {
        "dictionary": "update_dictionary.py",
        "literal": "update_literal.py",
        "main": "update_main.py",
        "explanation": "update_explanation.py",
        "rules": "update_rules.py"
    }
    
    print(f"--- Starting Master Forensic Sync for {batch_dir} ---")
    
    for field_key, script_name in fields.items():
        json_path = os.path.join(batch_dir, f"{field_key}.json")
        if os.path.exists(json_path):
            print(f"\n>> Running {script_name}...")
            # Use sys.executable to ensure we use the same python environment
            result = subprocess.run([sys.executable, script_name, json_path], capture_output=True, text=True)
            print(result.stdout)
            if result.stderr:
                print(f"Error in {script_name}: {result.stderr}")
        else:
            print(f"Skipping {field_key}: {json_path} not found.")

    print("\n--- Master Sync Complete ---")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python master_forensic.py <batch_directory>")
    else:
        run_all(sys.argv[1])
