# Tasklist - 命令列提醒事項管理工具

一個簡單好用的命令列待辦事項管理工具，支援優先級和到期日設定。

## 功能特色

- **新增任務** - 設定名稱、優先級和到期日
- **更新任務** - 修改任務名稱、優先級或到期日
- **標記完成** - 使用 `done` 標記為已完成
- **還原完成** - 使用 `undo` 標記為未完成
- **刪除任務** - 移除不再需要的任務
- **排序顯示** - 依到期日和優先級自動排序
- **逾期標記** - 逾期任務顯示 🔥 符號

## 安裝方式

不需要安裝，直接執行 Python 檔案即可：

```bash
python tasklist.py
```

## 使用說明

### 基本指令

```bash
# 顯示待辦事項列表
python tasklist.py

# 顯示所有事項（包含已完成）
python tasklist.py all
```

### 新增任務

```bash
# 格式：add <名稱> [優先級] [到期日]
# 優先級：1-5，5 為最重要（預設 3）
# 到期日格式：YYYY-MM-DD（預設今天）

python tasklist.py add "買牛奶"
python tasklist.py add "寫報告" 5 "2026-03-15"
python tasklist.py add "健身" 3
```

### 更新任務

```bash
# 格式：update <任務名稱或 ID> <新值>
# 系統會自動判斷更新內容

# 更新名稱
python tasklist.py update 1 "買蔬菜"

# 更新優先級（數字）
python tasklist.py update 1 5

# 更新到期日（日期格式）
python tasklist.py update 1 "2026-03-20"
```

### 標記完成/未完成

```bash
# 標記為已完成
python tasklist.py done <任務名稱或 ID>

# 標記為未完成
python tasklist.py undo <任務名稱或 ID>
```

### 刪除任務

```bash
# 格式：delete <任務名稱或 ID>
python tasklist.py delete <任務名稱或 ID>
```

## 儲存方式

任務資料自動儲存於 `tasks.json` 檔案。

## Claude Code Skill

本工具已整合至 Claude Code，可直接使用：

```
/tasklist add <任務名稱> [優先級] [到期日]
/tasklist all
/tasklist done <任務名稱或 ID>
/tasklist undo <任務名稱或 ID>
/tasklist delete <任務名稱或 ID>
```

