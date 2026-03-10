# 番茄长篇爽文项目

本仓库用于持续连载“东北系统爽文”章节，并保证：

- 每个章节单独保存为 `chapters/chapter_XXX.md`
- 每章字数严格在 **1500-2200**（按去除空白后的字符数）
- 章节元数据写入 `novel.db`

## 当前章节

- `chapter_001.md`
- `chapter_002.md`
- `chapter_003.md`

## 更新数据库

```bash
python3 tools/update_chapter_db.py
```

执行后会：

1. 校验所有章节字数区间
2. 将章节号、标题、路径、字数、章节末钩子写入 SQLite 表 `chapters`

## 查询示例

```bash
sqlite3 novel.db 'select chapter_no,title,char_count from chapters order by chapter_no;'
```
## 数据库文件说明

`novel.db` 为本地生成文件，不纳入 Git 版本管理（避免二进制文件上传失败）。
首次使用或章节更新后，请运行：

```bash
python3 tools/update_chapter_db.py
```


