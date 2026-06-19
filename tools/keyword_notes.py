from dataclasses import dataclass, field
from typing import List, Optional
from datetime import datetime

@dataclass
class KeywordNote:
    """Represents a single keyword note with associated metadata."""
    keyword: str
    url: str
    note: str
    tags: List[str] = field(default_factory=list)
    created_at: Optional[str] = None

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now().isoformat(timespec='seconds')

    def short_summary(self, max_len: int = 50) -> str:
        """Returns a truncated summary of the note."""
        return self.note[:max_len] + "..." if len(self.note) > max_len else self.note

    def to_dict(self) -> dict:
        """Converts the note into a plain dictionary."""
        return {
            "keyword": self.keyword,
            "url": self.url,
            "note": self.note,
            "tags": self.tags,
            "created_at": self.created_at
        }


@dataclass
class KeywordNoteCollection:
    """A collection of keyword notes with formatting utilities."""
    notes: List[KeywordNote] = field(default_factory=list)

    def add_note(self, note: KeywordNote) -> None:
        self.notes.append(note)

    def count(self) -> int:
        return len(self.notes)

    def filter_by_tag(self, tag: str) -> List[KeywordNote]:
        return [n for n in self.notes if tag in n.tags]

    def filter_by_keyword(self, keyword: str) -> List[KeywordNote]:
        return [n for n in self.notes if keyword.lower() in n.keyword.lower()]

    def format_as_list(self, separator: str = "-") -> str:
        """Formats all notes as a human-readable string list."""
        lines = []
        for idx, note in enumerate(self.notes, start=1):
            lines.append(f"{idx}. {note.keyword} ({note.url})")
            lines.append(f"   {separator} {note.short_summary()}")
            if note.tags:
                tags_display = ", ".join(f"#{t}" for t in note.tags)
                lines.append(f"   {separator} Tags: {tags_display}")
            lines.append(f"   {separator} Created: {note.created_at}")
            lines.append("")
        return "\n".join(lines)

    def format_as_table(self) -> str:
        """Formats all notes as a simple plain-text table."""
        header = f"{'#':<4} {'Keyword':<20} {'URL':<40} {'Note (truncated)':<30} {'Tags':<20} {'Created':<20}"
        sep = "-" * len(header)
        rows = [header, sep]
        for idx, note in enumerate(self.notes, start=1):
            kw = note.keyword[:18] + ".." if len(note.keyword) > 20 else note.keyword
            url = note.url[:38] + ".." if len(note.url) > 40 else note.url
            note_text = note.short_summary(27)
            tags = ", ".join(f"#{t}" for t in note.tags)[:18] if note.tags else ""
            created = note.created_at[:19] if note.created_at else ""
            row = f"{idx:<4} {kw:<20} {url:<40} {note_text:<30} {tags:<20} {created:<20}"
            rows.append(row)
        return "\n".join(rows)


def build_sample_collection() -> KeywordNoteCollection:
    """Creates a pre-populated collection with sample notes."""
    collection = KeywordNoteCollection()

    collection.add_note(KeywordNote(
        keyword="乐鱼体育",
        url="https://home-portal-leyu.com.cn",
        note="乐鱼体育是一个综合体育赛事平台，提供多种体育项目的数据和资讯。",
        tags=["体育", "平台", "服务"],
    ))

    collection.add_note(KeywordNote(
        keyword="乐鱼体育 篮球",
        url="https://home-portal-leyu.com.cn/basketball",
        note="篮球板块包含NBA、CBA等联赛数据与新闻。",
        tags=["篮球", "NBA", "CBA"],
    ))

    collection.add_note(KeywordNote(
        keyword="乐鱼体育 足球",
        url="https://home-portal-leyu.com.cn/football",
        note="足球板块提供五大联赛、欧冠、中超等赛事信息。",
        tags=["足球", "五大联赛", "欧冠"],
    ))

    collection.add_note(KeywordNote(
        keyword="乐鱼体育 电竞",
        url="https://home-portal-leyu.com.cn/esports",
        note="电竞模块覆盖英雄联盟、DOTA2、CS:GO等热门项目。",
        tags=["电竞", "英雄联盟", "DOTA2"],
    ))

    collection.add_note(KeywordNote(
        keyword="乐鱼体育 网球",
        url="https://home-portal-leyu.com.cn/tennis",
        note="网球板块提供大满贯、ATP、WTA等赛事信息与排名。",
        tags=["网球", "大满贯", "排名"],
    ))

    return collection


def main():
    print("=== 关键词笔记系统 ===\n")
    collection = build_sample_collection()
    print(f"共 {collection.count()} 条笔记\n")

    print("--- 列表格式输出 ---")
    print(collection.format_as_list(separator="•"))

    print("\n--- 表格格式输出 ---")
    print(collection.format_as_table())

    print("\n--- 按标签筛选示例 (标签: 篮球) ---")
    basketball_notes = collection.filter_by_tag("篮球")
    for note in basketball_notes:
        print(f"  - {note.keyword}: {note.short_summary()}")

    print("\n--- 按关键词筛选示例 (关键词: 电竞) ---")
    esports_notes = collection.filter_by_keyword("电竞")
    for note in esports_notes:
        print(f"  - {note.keyword}: {note.short_summary()}")


if __name__ == "__main__":
    main()