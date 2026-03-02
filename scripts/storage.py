import json
import os
from typing import List, Dict, Any


class Storage:
    DATA_FILE = 'tasks.json'
    TEMP_FILE = 'tasks.json.tmp'

    @classmethod
    def load_tasks(cls) -> List[Dict[str, Any]]:
        if not os.path.exists(cls.DATA_FILE):
            return []
        try:
            with open(cls.DATA_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return []

    @classmethod
    def save_tasks(cls, tasks: List[Dict[str, Any]]) -> bool:
        try:
            with open(cls.TEMP_FILE, 'w', encoding='utf-8') as f:
                json.dump(tasks, f, ensure_ascii=False, indent=2)
            os.replace(cls.TEMP_FILE, cls.DATA_FILE)
            return True
        except IOError:
            return False
