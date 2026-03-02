from typing import List
from models import Task
from storage import Storage
from display import Display
from datetime import datetime


class CommandHandler:
    def __init__(self):
        self.tasks = self._load_tasks()

    def _load_tasks(self) -> List[Task]:
        data = Storage.load_tasks()
        return [Task.from_dict(t) for t in data]

    def _save_tasks(self) -> bool:
        data = [t.to_dict() for t in self.tasks]
        return Storage.save_tasks(data)

    def _get_next_id(self) -> int:
        if not self.tasks:
            return 1
        return max(t.id for t in self.tasks) + 1

    def _find_task(self, task_id: int) -> Task:
        for task in self.tasks:
            if task.id == task_id:
                return task
        return None

    def execute(self, args: List[str]) -> str:
        if not args:
            return self._show_pending()

        command = args[0].lower()

        if command == 'add':
            return self._add_task(args[1:])
        elif command == 'update':
            return self._update_task(args[1:])
        elif command == 'done':
            return self._mark_done(args[1:])
        elif command == 'undo':
            return self._mark_undo(args[1:])
        elif command == 'delete':
            return self._delete_task(args[1:])
        elif command == 'all':
            return self._show_all()
        else:
            return f'未知指令: {command}'

    def _add_task(self, args: List[str]) -> str:
        if not args:
            return '請提供任務名稱'

        name = args[0]
        priority = 3
        due_date = None

        if len(args) > 1:
            try:
                priority = int(args[1])
                if not 1 <= priority <= 5:
                    return '優先級必須在 1-5 之間'
            except ValueError:
                pass

        if len(args) > 2:
            due_date = args[2]
            try:
                datetime.strptime(due_date, '%Y-%m-%d')
            except ValueError:
                return '日期格式錯誤，請使用 YYYY-M-D'

        task_id = self._get_next_id()
        task = Task.create(task_id, name, priority, due_date)
        self.tasks.append(task)
        self._save_tasks()
        result = f'已新增任務 [{task_id}] {name}\n\n'
        result += self._show_pending()
        return result

    def _update_task(self, args: List[str]) -> str:
        if len(args) < 2:
            return '請提供: update <事項名稱或ID> <新值>'

        task_identifier = args[0]
        new_value = args[1]

        # 嘗試用 ID 查找，失敗則用名稱查找
        task = None
        try:
            task_id = int(task_identifier)
            task = self._find_task(task_id)
        except ValueError:
            # 用名稱查找
            for t in self.tasks:
                if t.name == task_identifier:
                    task = t
                    break

        if not task:
            return f'找不到任務: {task_identifier}'

        # 判斷新值的類型
        if self._is_date(new_value):
            # 日期格式 -> 更新到期日
            task.due_date = new_value
            self._save_tasks()
            result = f'已更新任務 [{task.id}] {task.name} 的到期日為 {new_value}\n\n'
        elif new_value.isdigit():
            # 數值 -> 更新優先級
            priority = int(new_value)
            if not 1 <= priority <= 5:
                return '優先級必須在 1-5 之間'
            task.priority = priority
            self._save_tasks()
            result = f'已更新任務 [{task.id}] {task.name} 的優先級為 {priority}\n\n'
        else:
            # 其他文字 -> 更新名稱
            old_name = task.name
            task.name = new_value
            self._save_tasks()
            result = f'已更新任務名稱: {old_name} -> {new_value}\n\n'
        result += self._show_pending()
        return result

    def _is_date(self, value: str) -> bool:
        """檢查是否為 YYYY-M-D 或 YYYY-MM-DD 日期格式"""
        try:
            datetime.strptime(value, '%Y-%m-%d')
            return True
        except ValueError:
            return False

    def _mark_done(self, args: List[str]) -> str:
        if not args:
            return '請提供任務名稱或 ID'

        task_identifier = args[0]

        # 嘗試用 ID 查找，失敗則用名稱查找
        task = None
        try:
            task_id = int(task_identifier)
            task = self._find_task(task_id)
        except ValueError:
            # 用名稱查找
            for t in self.tasks:
                if t.name == task_identifier:
                    task = t
                    break

        if not task:
            return f'找不到任務: {task_identifier}'

        task.status = '已完成'
        self._save_tasks()
        result = f'已將任務 [{task.id}] {task.name} 標記為已完成\n\n'
        result += self._show_pending()
        return result

    def _mark_undo(self, args: List[str]) -> str:
        if not args:
            return '請提供任務名稱或 ID'

        task_identifier = args[0]

        # 嘗試用 ID 查找，失敗則用名稱查找
        task = None
        try:
            task_id = int(task_identifier)
            task = self._find_task(task_id)
        except ValueError:
            # 用名稱查找
            for t in self.tasks:
                if t.name == task_identifier:
                    task = t
                    break

        if not task:
            return f'找不到任務: {task_identifier}'

        task.status = '未完成'
        self._save_tasks()
        result = f'已將任務 [{task.id}] {task.name} 標記為未完成\n\n'
        result += self._show_pending()
        return result

    def _delete_task(self, args: List[str]) -> str:
        if not args:
            return '請提供任務名稱或 ID'

        task_identifier = args[0]

        # 嘗試用 ID 查找，失敗則用名稱查找
        task = None
        try:
            task_id = int(task_identifier)
            task = self._find_task(task_id)
        except ValueError:
            # 用名稱查找
            for t in self.tasks:
                if t.name == task_identifier:
                    task = t
                    break

        if not task:
            return f'找不到任務: {task_identifier}'

        self.tasks.remove(task)
        self._save_tasks()
        result = f'已刪除任務 [{task.id}] {task.name}\n\n'
        result += self._show_pending()
        return result

    def _show_pending(self) -> str:
        pending = [t for t in self.tasks if t.status == '未完成']
        return Display.format_tasks(pending, show_completed=False)

    def _show_all(self) -> str:
        return Display.format_tasks(self.tasks, show_completed=True)
