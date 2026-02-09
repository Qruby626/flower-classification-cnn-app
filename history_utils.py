import json
import os
from datetime import datetime

HISTORY_FILE = 'data/history.json'

def init_history():
    if not os.path.exists('data'):
        os.makedirs('data')
    if not os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, 'w') as f:
            json.dump([], f)

def get_history():
    init_history()
    try:
        with open(HISTORY_FILE, 'r') as f:
            return json.load(f)
    except Exception:
        return []

def add_to_history(filename, label, confidence, is_recognized):
    init_history()
    history = get_history()
    
    new_entry = {
        "id": len(history) + 1,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "filename": filename,
        "label": label,
        "confidence": confidence,
        "is_recognized": is_recognized
    }
    
    # Keep only the last 50 entries
    history.insert(0, new_entry)
    history = history[:50]
    
    with open(HISTORY_FILE, 'w') as f:
        json.dump(history, f, indent=4)

def clear_history():
    init_history()
    # Rule 7: Delete physical files to ensure privacy
    history = get_history()
    upload_folder = 'static/uploads'
    
    for item in history:
        try:
            # maintain security by only deleting files in uploads folder
            filename = item.get('filename')
            if filename:
                filepath = os.path.join(upload_folder, filename)
                if os.path.exists(filepath):
                    os.remove(filepath)
                
                # Try to remove heatmap if exists
                h_filename = "heatmap_" + filename
                h_filepath = os.path.join(upload_folder, h_filename)
                if os.path.exists(h_filepath):
                    os.remove(h_filepath)
        except Exception as e:
            print(f"Error deleting file {filename}: {e}")

    with open(HISTORY_FILE, 'w') as f:
        json.dump([], f)
