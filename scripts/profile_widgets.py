"""Render profile widgets from public GitHub data, using only the standard library."""

import argparse
from collections import Counter
from datetime import datetime, timezone
from html import escape
import json
import os
from pathlib import Path
import re
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen
from zoneinfo import ZoneInfo


ROOT = Path(__file__).resolve().parents[1]
PALETTE = ("#79B8FF", "#B4A1FF", "#7EE7C0", "#F0CA81", "#ADBAC7")


def request_json(path):
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "github-profile-widgets",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    if token := os.environ.get("GITHUB_TOKEN"):
        headers["Authorization"] = f"Bearer {token}"
    with urlopen(Request(f"https://api.github.com/{path}", headers=headers), timeout=30) as response:
        return json.load(response)


def own_public_repositories(repositories, username):
    return [
        repo for repo in repositories
        if repo.get("private") is False
        and not repo.get("fork", True)
        and repo.get("owner", {}).get("login", "").casefold() == username.casefold()
    ]


def collect(username):
    repositories = []
    page = 1
    while True:
        # This endpoint lists public repositories, even when authenticated.
        batch = request_json(f"users/{username}/repos?type=owner&per_page=100&page={page}")
        repositories.extend(batch)
        if len(batch) < 100:
            break
        page += 1

    repositories = own_public_repositories(repositories, username)
    languages = Counter()
    for repo in repositories:
        result = request_json(f"repos/{username}/{repo['name']}/languages")
        for language, size in result.items():
            if isinstance(size, int) and size > 0:
                languages[language] += size

    return {
        "username": username,
        "updated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "scope": "public repositories owned by the account; forks excluded",
        "repositories": len(repositories),
        "stars": sum(repo.get("stargazers_count", 0) for repo in repositories),
        "languages": dict(sorted(languages.items(), key=lambda item: (-item[1], item[0]))),
        "sources": [
            f"https://api.github.com/users/{username}/repos",
            "https://docs.github.com/en/rest/repos/repos#list-repository-languages",
        ],
    }


def text(x, y, value, *, size=14, color="#ADBAC7", weight=400, anchor="start"):
    return (
        f'<text x="{x}" y="{y}" font-size="{size}" fill="{color}" '
        f'font-weight="{weight}" text-anchor="{anchor}">{escape(str(value))}</text>'
    )


def card(title, description, content):
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" width="420" height="240" '
        'viewBox="0 0 420 240" role="img" aria-labelledby="title description">\n'
        f'<title id="title">{escape(title)}</title>\n'
        f'<desc id="description">{escape(description)}</desc>\n'
        '<rect x=".5" y=".5" width="419" height="239" rx="14" fill="#151B23" stroke="#3D444D"/>\n'
        '<g font-family="-apple-system,BlinkMacSystemFont,Segoe UI,Helvetica,Arial,sans-serif">\n'
        + "\n".join(content) + '\n</g>\n</svg>\n'
    )


def overview(data, language):
    es = language == "es"
    title = "Mi trabajo en GitHub" if es else "My work on GitHub"
    labels = ("Repositorios", "Estrellas", "Lenguajes") if es else ("Repositories", "Stars", "Languages")
    values = (data["repositories"], data["stars"], len(data["languages"]))
    description = "; ".join(f"{label}: {value}" for label, value in zip(labels, values))
    date = datetime.fromisoformat(data["updated_at"]).astimezone(ZoneInfo("America/Santiago")).strftime("%Y-%m-%d")
    content = [
        text(24, 30, "GITHUB / OPEN SOURCE", size=12, color="#79B8FF", weight=600),
        text(24, 62, title, size=23, color="#F0F6FC", weight=600),
        '<path d="M24 80h372" stroke="#3D444D"/>',
    ]
    for x, label, value, color in zip((24, 164, 292), labels, values, PALETTE):
        content.extend([
            text(x, 133, value, size=42, color=color, weight=600),
            text(x, 160, label, size=15),
        ])
    content.extend([
        text(24, 197, "Solo repositorios públicos propios · Sin forks" if es else "Own public repositories only · No forks", size=13),
        text(24, 221, ("Actualizado" if es else "Updated") + f" {date}", size=12),
        '<circle cx="388" cy="217" r="4" fill="#7EE7C0"/>',
    ])
    return card(title, description, content)


def language_rows(languages, language):
    ordered = sorted(languages.items(), key=lambda item: (-item[1], item[0]))
    rows = ordered[:4]
    if len(ordered) > 4:
        rows.append(("Otros" if language == "es" else "Other", sum(value for _, value in ordered[4:])))
    return rows


def language_chart(data, language):
    es = language == "es"
    title = "Lenguajes del código" if es else "Languages in my code"
    rows = language_rows(data["languages"], language)
    total = sum(data["languages"].values())
    content = [
        text(24, 30, "GITHUB / CODE MIX", size=12, color="#79B8FF", weight=600),
        text(24, 62, title, size=23, color="#F0F6FC", weight=600),
    ]
    description = []
    for index, (name, size) in enumerate(rows):
        y = 91 + index * 23
        percent = size / total * 100
        content.extend([
            text(24, y + 4, name, size=14, color="#F0F6FC"),
            f'<rect x="143" y="{y - 5}" width="190" height="8" rx="4" fill="#28323E"/>',
            f'<rect x="143" y="{y - 5}" width="{190 * percent / 100:.2f}" height="8" rx="4" fill="{PALETTE[index]}"/>',
            text(396, y + 4, f"{percent:.1f}%", size=13, anchor="end"),
        ])
        description.append(f"{name}: {percent:.1f}%")
    if not rows:
        content.append(text(24, 123, "Aún no hay código público." if es else "No public code yet.", size=16))
    content.append(text(24, 221, "Bytes de código · Sin forks" if es else "Code bytes · Forks excluded", size=13))
    return card(title, "; ".join(description) or title, content)


def render(data):
    files = {"github-data.json": json.dumps(data, ensure_ascii=False, indent=2) + "\n"}
    for language in ("es", "en"):
        files[f"overview-{language}.svg"] = overview(data, language)
        files[f"languages-{language}.svg"] = language_chart(data, language)
    return files


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--username", default="Martin-Ferreira-O")
    parser.add_argument("--output", type=Path, default=ROOT / "assets" / "widgets")
    args = parser.parse_args()
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9-]{0,38}", args.username):
        parser.error("Invalid GitHub username")
    try:
        # Fetch and render everything before touching the last successful snapshot.
        files = render(collect(args.username))
    except (HTTPError, URLError, TimeoutError, ValueError, TypeError, KeyError) as error:
        status = f"HTTP {error.code}" if isinstance(error, HTTPError) else type(error).__name__
        raise SystemExit(f"GitHub data unavailable ({status}); existing widgets were preserved.") from None
    args.output.mkdir(parents=True, exist_ok=True)
    for name, content in files.items():
        target = args.output / name
        temporary = target.with_suffix(target.suffix + ".tmp")
        temporary.write_text(content, encoding="utf-8")
        temporary.replace(target)
    print(f"Updated {len(files)} public-data widget files.")


if __name__ == "__main__":
    main()
