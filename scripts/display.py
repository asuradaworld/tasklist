from typing import List
from datetime import datetime
from models import Task


class Display:
    EMERGENCY_EMOJI = '🔥'

    @classmethod
    def format_tasks(cls, tasks: List[Task], show_completed: bool = False) -> str:
        if not tasks:
            return '沒有提醒事項'

        sorted_tasks = cls._sort_tasks(tasks)

        if not show_completed:
            sorted_tasks = [t for t in sorted_tasks if t.status == '未完成']

        if not sorted_tasks and not show_completed:
            return '沒有待辦事項'

        lines = ['———————————————', 'Tasklist提醒事項:', '']

        if show_completed:
            pending = [t for t in sorted_tasks if t.status == '未完成']
            completed = [t for t in sorted_tasks if t.status == '已完成']

            task_lines = []
            for task in pending:
                task_lines.extend(cls._format_task(task))
                task_lines.append('')
            lines.extend(task_lines)

            if completed:
                lines.append('')
                lines.append('——— 已完成 ———')
                lines.append('')
                task_lines = []
                for task in completed:
                    task_lines.extend(cls._format_task(task))
                    task_lines.append('')
                lines.extend(task_lines)
        else:
            task_lines = []
            for task in sorted_tasks:
                task_lines.extend(cls._format_task(task))
                task_lines.append('')
            lines.extend(task_lines)

        lines.append('———————————————')
        return '\n'.join(lines)

    @classmethod
    def _format_task(cls, task: Task) -> List[str]:
        name = task.name
        if task.status == '未完成' and cls._is_overdue(task.due_date):
            name = f"{cls.EMERGENCY_EMOJI}{name}"

        # 統一格式化日期為 yyyy-mm-dd
        formatted_date = cls._format_date(task.due_date)

        return [
            f"{task.id}. {name}",
            f"{task.priority} {formatted_date}"
        ]

    @classmethod
    def _format_date(cls, due_date: str) -> str:
        """將日期統一格式化為 yyyy-mm-dd"""
        try:
            dt = datetime.strptime(due_date, '%Y-%m-%d')
            return dt.strftime('%Y-%m-%d')
        except ValueError:
            return due_date

    @classmethod
    def _is_overdue(cls, due_date: str) -> bool:
        try:
            due = datetime.strptime(due_date, '%Y-%m-%d')
            today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
            return due < today
        except ValueError:
            return False

    @classmethod
    def _sort_tasks(cls, tasks: List[Task]) -> List[Task]:
        today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)

        def sort_key(task: Task) -> tuple:
            try:
                due = datetime.strptime(task.due_date, '%Y-%m-%d')
            except ValueError:
                due = today

            is_overdue = due < today and task.status == '未完成'
            days_overdue = (today - due).days if is_overdue else 0
            days_until = (due - today).days if not is_overdue else 999999

            return (
                0 if is_overdue else 1,
                -days_overdue if is_overdue else days_until,
                -task.priority
            )

        return sorted(tasks, key=sort_key)
