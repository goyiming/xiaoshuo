# 番茄长篇爽文项目

本仓库用于持续连载“东北系统爽文”章节，并保证：

- 每个章节单独保存为 `chapters/章节名称.md`（例如：`第7章 XXX.md`）
- 每章字数严格在 **1500-2200**（按去除空白后的字符数）
- 章节元数据写入 `novel.db`

## 当前章节

- `第1章 破屋里的系统提示音.md`
- `第2章 竞标桌上掀翻地头蛇.md`
- `第3章 冰河突围，第一批山货进城.md`
- `第4章 检查站夜局，反手拿到把柄.md`
- `第5章 废仓库交易，挖出第一条暗线.md`
- `第6章 复核会翻盘，拿下县里第一单.md`

## 更新数据库

```bash
python3 tools/update_chapter_db.py
```

执行后会：

1. 校验所有章节字数区间
2. 从标题/文件名中的“第X章”解析章节号
3. 将章节号、标题、路径、字数、章节末钩子写入 SQLite 表 `chapters`

## 查询示例

```bash
sqlite3 novel.db 'select chapter_no,title,file_path,char_count from chapters order by chapter_no;'
```

## 数据库文件说明

`novel.db` 为本地生成文件，不纳入 Git 版本管理（避免二进制文件上传失败）。
首次使用或章节更新后，请运行：

```bash
python3 tools/update_chapter_db.py
```
