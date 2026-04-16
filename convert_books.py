#!/usr/bin/env python3
"""Convert Obsidian book notes from og-vault into Hugo content pages."""

import re
from pathlib import Path

VAULT_BOOKS = Path("/home/dmdecke/notworkplace/og-vault/02 - Areas/BOOKS")
CONTENT_BOOKS = Path("/home/dmdecke/notworkplace/ddecks/content/books")


def slugify(name: str) -> str:
    s = name.lower().strip()
    s = re.sub(r"[^\w\s-]", "", s)
    s = re.sub(r"[\s_]+", "-", s)
    s = re.sub(r"-+", "-", s)
    return s.strip("-")


def parse_front_matter(text: str) -> tuple[dict, str]:
    m = re.match(r"^---\n(.*?)\n---\n(.*)", text, re.DOTALL)
    if not m:
        return {}, text
    raw, body = m.group(1), m.group(2).strip()
    meta: dict = {}
    lines = raw.split("\n")
    i = 0
    while i < len(lines):
        line = lines[i]
        # YAML list item under a key (e.g. "  - self-help")
        if re.match(r"^\s+-\s+", line):
            i += 1
            continue
        if ":" not in line:
            i += 1
            continue
        key, val = line.split(":", 1)
        key = key.strip()
        val = val.strip()
        # Handle inline array: Tags: [interview, software, system-design, learning]
        if val.startswith("[") and val.endswith("]"):
            items = [v.strip().strip('"').strip("'").lstrip("#") for v in val[1:-1].split(",") if v.strip()]
            meta[key] = items
            i += 1
            continue
        # Strip surrounding quotes
        val = val.strip('"').strip("'")
        # Value is empty — could be a multi-line value or YAML list
        if not val:
            # Peek ahead for indented continuation (value or list)
            collected_list = []
            j = i + 1
            while j < len(lines) and re.match(r"^\s+", lines[j]):
                stripped = lines[j].strip()
                if stripped.startswith("- "):
                    item = stripped[2:].strip().strip('"').strip("'").lstrip("#")
                    collected_list.append(item)
                elif stripped:
                    # Indented continuation value (e.g. Title on next line)
                    val = stripped.strip('"').strip("'")
                j += 1
            if collected_list:
                meta[key] = collected_list
            elif val:
                meta[key] = val
            else:
                meta[key] = ""
            i = j
            continue
        # Single hashtag tag value: Tags: #carpedeim
        if key.lower() == "tags" and val.startswith("#"):
            meta[key] = [v.strip().lstrip("#") for v in val.split() if v.strip()]
            i += 1
            continue
        meta[key] = val
        i += 1
    return meta, body


def clean_body(body: str, title: str) -> str:
    body = re.sub(r"^#\s+" + re.escape(title) + r"\s*$", "", body, flags=re.MULTILINE)
    body = re.sub(r"^#\s+Title:\s+" + re.escape(title) + r"\s*$", "", body, flags=re.MULTILINE)
    body = re.sub(r"^(Cover|URL)::?\s*.*$", "", body, flags=re.MULTILINE)
    body = re.sub(r">\s*\[!Started:.*?Finished:.*?\]", "", body)
    body = re.sub(r">\s*\[!(.*?)\]", r"> **\1**", body)
    body = re.sub(r"\[\[([^\]|]+?)(?:\|([^\]]+?))?\]\]", lambda m: m.group(2) or m.group(1), body)
    body = re.sub(r"!\[Cover\]\(\)\s*", "", body)
    body = re.sub(r"\n{3,}", "\n\n", body)
    return body.strip()


def esc(s: str) -> str:
    return s.replace("\\", "\\\\").replace('"', '\\"')


def to_hugo_page(meta: dict, body: str, genre: str, filename: str = "") -> str:
    title = meta.get("Title", "") or filename.replace("_", " ") or "Untitled"
    author = meta.get("Author", "")
    publish_date = meta.get("Publish date", "")
    rating = meta.get("Rating", "")
    recommender = meta.get("Recommender", "")
    status = meta.get("Status", "")
    tags = meta.get("Tags") or meta.get("tags") or []
    if isinstance(tags, str):
        tags = [t.strip().lstrip("#") for t in tags.split(",") if t.strip()]
    # Add status as a tag
    if status and status not in tags:
        tags.append(status)
    # Use Created date from vault
    date = meta.get("Created", "") or meta.get("created", "") or meta.get("Date", "")
    if isinstance(date, str):
        # Strip wrapping like 'created: 2024-08-26'
        date = re.sub(r"^created:\s*", "", date).strip('"').strip("'")
        date = date.split(" ")[0]

    lines = ["+++"]
    lines.append(f'title = "{esc(title)}"')
    if date and re.match(r"^\d{4}-\d{2}-\d{2}$", date):
        lines.append(f'date = "{date}"')
    if tags:
        tag_str = ", ".join(f'"{esc(t)}"' for t in tags)
        lines.append(f"tags = [{tag_str}]")
    lines.append("[params]")
    if author:
        lines.append(f'  author = "{esc(author)}"')
    if publish_date:
        lines.append(f'  publish_date = "{esc(publish_date)}"')
    if rating and rating != "/10":
        try:
            lines.append(f"  rating = {int(rating)}")
        except (ValueError, TypeError):
            lines.append(f'  rating = "{esc(str(rating))}"')
    if recommender:
        lines.append(f'  recommender = "{esc(recommender)}"')
    if status:
        lines.append(f'  status = "{esc(status)}"')
    if genre:
        lines.append(f'  genre = "{genre}"')
    lines.append("+++")
    lines.append("")

    cleaned = clean_body(body, title)
    if cleaned:
        lines.append(cleaned)

    return "\n".join(lines) + "\n"


def main():
    count = 0
    genres = {}
    for genre_dir in sorted(VAULT_BOOKS.iterdir()):
        if not genre_dir.is_dir() or genre_dir.name.startswith("."):
            continue
        genre_slug = slugify(genre_dir.name)
        out_dir = CONTENT_BOOKS / genre_slug
        out_dir.mkdir(parents=True, exist_ok=True)
        genre_count = 0

        for md_file in sorted(genre_dir.glob("*.md")):
            text = md_file.read_text(encoding="utf-8")
            meta, body = parse_front_matter(text)
            if not meta:
                continue
            hugo_content = to_hugo_page(meta, body, genre_slug, md_file.stem)
            slug = slugify(md_file.stem)
            out_path = out_dir / f"{slug}.md"
            out_path.write_text(hugo_content, encoding="utf-8")
            count += 1
            genre_count += 1

        genres[genre_slug] = genre_count

    (CONTENT_BOOKS / "_index.md").write_text(
        '+++\ntitle = "Books"\nweight = 5\n+++\n\nBook notes and reviews organized by genre.\n'
    )

    labels = {"fantasy": "Fantasy", "fiction": "Fiction", "nonfiction": "Nonfiction",
              "scifi": "Sci-Fi", "webnovel": "Webnovel"}
    for slug in sorted(d.name for d in CONTENT_BOOKS.iterdir() if d.is_dir()):
        label = labels.get(slug, slug.title())
        (CONTENT_BOOKS / slug / "_index.md").write_text(f'+++\ntitle = "{label}"\n+++\n')

    print(f"Converted {count} books into {CONTENT_BOOKS}")
    for g, c in sorted(genres.items()):
        print(f"  {g}: {c}")


if __name__ == "__main__":
    main()
