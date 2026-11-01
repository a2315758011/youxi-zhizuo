#!/usr/bin/env python3
"""游戏制作资料库轻量质量检查。仅使用 Python 标准库。"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit

SKILL_COUNT_RE = re.compile(r"当前仓库技能规模：\s*(\d+)\s*份\s*SKILL\.md")
NAME_RE = re.compile(r"(?m)^name:\s*[^\s#].*$")
DESCRIPTION_RE = re.compile(r"(?m)^description:\s*(?:\S.*)?$")
LINK_RE = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
CORE_DOCS = (
    "README.md",
    "AGENTS.md",
    "程序开发/AI游戏代码工程总规范/SKILL.md",
    "外部专业技能库/everything-game-dev-code/README.md",
    "外部专业技能库/awesome-copilot/README.md",
)


def resolve_local_link(source: Path, raw_target: str) -> Path | None:
    target = raw_target.strip().split(maxsplit=1)[0].strip("<>")
    parsed = urlsplit(target)
    if parsed.scheme or parsed.netloc or not parsed.path:
        return None
    return (source.parent / unquote(parsed.path)).resolve()


def main() -> int:
    parser = argparse.ArgumentParser(description="游戏仓库轻量质量检查")
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    root = parser.parse_args().root.resolve()
    errors: list[str] = []

    if not (root / "README.md").is_file():
        print(f"FAIL 仓库根目录缺少 README.md：{root}")
        return 2

    skill_files = sorted(root.rglob("SKILL.md"))
    for path in skill_files:
        content = path.read_text(encoding="utf-8")
        if not content.startswith("---\n"):
            errors.append(f"技能缺少 YAML frontmatter：{path.relative_to(root)}")
            continue
        header = content.split("---\n", 2)[1] if content.count("---\n") >= 2 else ""
        if not NAME_RE.search(header):
            errors.append(f"技能缺少 name：{path.relative_to(root)}")
        if not DESCRIPTION_RE.search(header):
            errors.append(f"技能缺少 description：{path.relative_to(root)}")

    readme = (root / "README.md").read_text(encoding="utf-8")
    match = SKILL_COUNT_RE.search(readme)
    if not match:
        errors.append("README.md 未找到可核对的 SKILL.md 总数声明")
    elif int(match.group(1)) != len(skill_files):
        errors.append(f"技能数量不一致：README 声明 {match.group(1)}，实际 {len(skill_files)}")

    for relative in CORE_DOCS:
        source = root / relative
        if not source.is_file():
            errors.append(f"核心索引文件缺失：{relative}")
            continue
        in_fence = False
        for line_no, line in enumerate(source.read_text(encoding="utf-8").splitlines(), 1):
            if line.lstrip().startswith(("\x60\x60\x60", "~~~")):
                in_fence = not in_fence
                continue
            if in_fence:
                continue
            for link in LINK_RE.findall(line):
                target = resolve_local_link(source, link)
                if target is None:
                    continue
                try:
                    target.relative_to(root)
                except ValueError:
                    errors.append(f"本地链接越出仓库：{relative}:{line_no} -> {link}")
                    continue
                if not target.exists():
                    errors.append(f"本地链接失效：{relative}:{line_no} -> {link}")

    for error in errors:
        print(f"FAIL {error}")
    if errors:
        print(f"\n检查失败：{len(errors)} 项；技能文件 {len(skill_files)} 份")
        return 1

    print(f"PASS 技能元数据：{len(skill_files)} 份")
    print("PASS README 技能数量与实际文件一致")
    print(f"PASS 核心索引本地链接：{len(CORE_DOCS)} 个文件")
    print("\n检查通过：0 项错误")
    return 0


if __name__ == "__main__":
    sys.exit(main())
