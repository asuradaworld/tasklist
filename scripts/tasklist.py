#!/usr/bin/env python3
"""Tasklist CLI - 命令列提醒事項管理工具"""

import sys
from commands import CommandHandler


def main():
    handler = CommandHandler()
    args = sys.argv[1:]
    result = handler.execute(args)
    print(result)


if __name__ == '__main__':
    main()
