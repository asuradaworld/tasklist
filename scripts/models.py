from dataclasses import dataclass, asdict
from typing import Dict, Any
from datetime import datetime


@dataclass
class Task:
    id: int
    name: str
    priority: int
    due_date: str
    status: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Task':
        return cls(
            id=data['id'],
            name=data['name'],
            priority=data['priority'],
            due_date=data['due_date'],
            status=data['status']
        )

    @classmethod
    def create(cls, task_id: int, name: str, priority: int = 3, due_date: str = None) -> 'Task':
        if due_date is None:
            due_date = datetime.now().strftime('%Y-%m-%d')
        return cls(
            id=task_id,
            name=name,
            priority=priority,
            due_date=due_date,
            status='未完成'
        )
