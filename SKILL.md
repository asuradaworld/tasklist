---
name: /tasklist
description: 命令列提醒事項管理工具 - 新增、修改、刪除和查看待辦事項
command: python scripts/tasklist.py
args:
  - name: action
    description: 操作類型 (add, update, done, delete, all 或留空顯示未完成事項)
    required: false
  - name: args
    description: 操作參數
    required: false
usage: |
  /tasklist                    - 顯示未完成事項
  /tasklist all                - 顯示所有事項
  /tasklist add <名稱> [優先級] [到期日] - 新增事項
  /tasklist update <事項名稱或ID> <新值>  - 更新事項 (依新值類型自動判斷)
  /tasklist done <事項名稱或ID>           - 標記完成/未完成
  /tasklist delete <事項名稱或ID>         - 刪除事項
---

# Tasklist Skill

提醒事項管理工具，支援優先級和到期日設定。

## 資料欄位

- **名稱**: 事項描述 (必填)
- **優先級**: 1-5，5 為最重要，預設 3
- **到期日**: YYYY-M-D 格式，預設今天
- **狀態**: 已完成/未完成

## 顯示規則

- 逾期事項標記 🔥 並優先顯示
- 依到期日排序，相同到期日依優先級排序
- 預設隱藏已完成事項
