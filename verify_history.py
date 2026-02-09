import os
import json
from history_utils import add_to_history, get_history, clear_history

def verify_history():
    print("Testing History Feature...")
    
    # 1. Clear existing history
    clear_history()
    print("History cleared.")
    
    # 2. Add sample entries
    add_to_history("rose.jpeg", "Rose", 95.5, True)
    add_to_history("test_cat.jpg", "Bukan Bunga / Tidak Dikenali", 12.3, False)
    print("Sample entries added.")
    
    # 3. Retrieve and verify
    history = get_history()
    print(f"History count: {len(history)}")
    
    if len(history) == 2:
        print("PASS: History count matches.")
        print(f"Top entry: {history[0]['label']} ({history[0]['confidence']}%)")
    else:
        print("FAIL: History count mismatch.")
        
    # 4. Check JSON file existence
    if os.path.exists('data/history.json'):
        print("PASS: history.json exists.")
    else:
        print("FAIL: history.json missing.")

if __name__ == "__main__":
    verify_history()
