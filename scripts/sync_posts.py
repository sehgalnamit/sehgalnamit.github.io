"""Syncs articles from articles.namitsehgal.com (Hashnode) into _posts as Jekyll markdown.

Idempotent: skips posts whose Hashnode guid is already recorded in an existing
_posts/*.md front matter (hashnode_url field).
"""
import re
import xml.etree.ElementTree as ET
from pathlib import Path

import requests
from markdownify import markdownify as md

RSS_URL = "https://articles.namitsehgal.com/rss.xml"
POSTS_DIR = Path(__file__).resolve().parent.parent / "_posts"


def slugify_from_link(link: str) -> str:
    return link.rstrip("/").rsplit("/", 1)[-1]


def existing_hashnode_urls() -> set[str]:
    urls = set()
    for md_file in POSTS_DIR.glob("*.md"):
        text = md_file.read_text(encoding="utf-8")
        match = re.search(r"^hashnode_url:\s*(\S+)\s*$", text, re.MULTILINE)
        if match:
            urls.add(match.group(1))
    return urls


def escape_yaml(value: str) -> str:
    return value.replace('"', '\\"')


def build_front_matter(title: str, date_str: str, link: str, excerpt: str) -> str:
    return (
        "---\n"
        "layout: post\n"
        f'title: "{escape_yaml(title)}"\n'
        f"date: {date_str}\n"
        "author: Namit Sehgal\n"
        f'excerpt: "{escape_yaml(excerpt)}"\n'
        f"hashnode_url: {link}\n"
        "---\n\n"
    )


def main() -> None:
    resp = requests.get(RSS_URL, timeout=30)
    resp.raise_for_status()
    root = ET.fromstring(resp.content)

    ns = {"content": "http://purl.org/rss/1.0/modules/content/"}
    already_synced = existing_hashnode_urls()
    created = []

    for item in root.findall(".//item"):
        link = item.findtext("link", "").strip()
        if not link or link in already_synced:
            continue

        title = re.sub(r"\s+", " ", item.findtext("title", "").strip())
        description = re.sub(r"\s+", " ", (item.findtext("description", "") or "").strip())
        pub_date_raw = item.findtext("pubDate", "").strip()
        content_el = item.find("content:encoded", ns)
        html_content = (content_el.text or "").strip() if content_el is not None else ""

        # e.g. "Fri, 14 Aug 2026 01:16:39 GMT" -> "2026-08-14"
        import email.utils as eut
        parsed = eut.parsedate_to_datetime(pub_date_raw)
        date_str = parsed.strftime("%Y-%m-%d")

        slug = slugify_from_link(link)
        filename = POSTS_DIR / f"{date_str}-{slug}.md"
        if filename.exists():
            continue

        markdown_body = md(html_content, heading_style="ATX")
        front_matter = build_front_matter(title, date_str, link, description)
        filename.write_text(front_matter + markdown_body.strip() + "\n", encoding="utf-8")
        created.append(filename.name)

    print(f"Created {len(created)} new post(s):")
    for name in created:
        print(f"  - {name}")


if __name__ == "__main__":
    main()
