#!/usr/bin/env python3
"""Crawl public jup-ag repositories for Gum/JupNet utility clues."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import urllib.request
from pathlib import Path
from typing import Any


DEFAULT_TERMS = (
    "gum",
    "dove",
    "jupnet",
    "bls",
    "bn254",
    "merkle",
    "crosschain",
    "proof_hash",
    "inbox",
    "outbox",
)

SKIP_DIRS = {
    ".git",
    ".next",
    ".turbo",
    "build",
    "coverage",
    "dist",
    "generated",
    "node_modules",
    "target",
    "vendor",
}

TEXT_SUFFIXES = {
    ".c",
    ".cc",
    ".cfg",
    ".conf",
    ".cpp",
    ".cs",
    ".css",
    ".go",
    ".graphql",
    ".h",
    ".hpp",
    ".html",
    ".java",
    ".js",
    ".json",
    ".jsx",
    ".kt",
    ".lock",
    ".md",
    ".mjs",
    ".proto",
    ".py",
    ".rb",
    ".rs",
    ".sh",
    ".sol",
    ".swift",
    ".toml",
    ".ts",
    ".tsx",
    ".txt",
    ".yaml",
    ".yml",
}

TEXT_FILENAMES = {
    "cargo.lock",
    "cargo.toml",
    "dockerfile",
    "makefile",
    "package-lock.json",
    "package.json",
    "pnpm-lock.yaml",
    "readme",
    "readme.md",
    "yarn.lock",
}


def compile_term_patterns(terms: tuple[str, ...]) -> dict[str, re.Pattern[str]]:
    return {
        term: re.compile(rf"(?<![A-Za-z0-9]){re.escape(term)}(?![A-Za-z0-9])", re.IGNORECASE)
        for term in terms
    }


def fetch_json(url: str) -> Any:
    request = urllib.request.Request(
        url,
        headers={
            "Accept": "application/vnd.github+json",
            "User-Agent": "gum-research-repo-crawler",
        },
    )
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        request.add_header("Authorization", f"Bearer {token}")
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.loads(response.read().decode("utf-8"))


def fetch_public_repos(org: str) -> list[dict[str, Any]]:
    repos: list[dict[str, Any]] = []
    page = 1
    while True:
        data = fetch_json(
            f"https://api.github.com/orgs/{org}/repos?per_page=100&page={page}&type=public"
        )
        if not data:
            break
        repos.extend(data)
        page += 1
    return sorted(repos, key=lambda repo: repo["full_name"].lower())


def run(command: list[str], cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        command,
        cwd=cwd,
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=180,
    )


def clone_repo(repo: dict[str, Any], dest: Path) -> tuple[bool, str]:
    result = run(
        [
            "git",
            "clone",
            "--depth",
            "1",
            "--filter=blob:limit=1048576",
            "--quiet",
            repo["clone_url"],
            str(dest),
        ]
    )
    if result.returncode == 0:
        return True, ""
    return False, (result.stderr or result.stdout).strip()


def is_text_candidate(path: Path, max_file_bytes: int) -> bool:
    try:
        if path.stat().st_size > max_file_bytes:
            return False
    except OSError:
        return False
    return path.name.lower() in TEXT_FILENAMES or path.suffix.lower() in TEXT_SUFFIXES


def scan_repo(repo_dir: Path, terms: tuple[str, ...], max_file_bytes: int) -> dict[str, Any]:
    patterns = compile_term_patterns(terms)
    term_counts = {term: 0 for term in terms}
    hits: list[dict[str, Any]] = []
    scanned_files = 0

    for root, dirs, files in os.walk(repo_dir):
        dirs[:] = [dirname for dirname in dirs if dirname.lower() not in SKIP_DIRS]
        for filename in files:
            path = Path(root) / filename
            if not is_text_candidate(path, max_file_bytes):
                continue
            rel = path.relative_to(repo_dir).as_posix()
            try:
                text = path.read_text(encoding="utf-8", errors="ignore")
            except OSError:
                continue
            scanned_files += 1
            for line_number, line in enumerate(text.splitlines(), start=1):
                matched = [term for term, pattern in patterns.items() if pattern.search(line)]
                if not matched:
                    continue
                for term in matched:
                    term_counts[term] += 1
                if len(hits) < 80:
                    snippet = " ".join(line.strip().split())
                    hits.append(
                        {
                            "path": rel,
                            "line": line_number,
                            "terms": matched,
                            "snippet": snippet[:240],
                        }
                    )

    return {
        "scanned_files": scanned_files,
        "term_counts": {term: count for term, count in term_counts.items() if count},
        "hits": hits,
    }


def write_markdown(
    output_path: Path,
    repos: list[dict[str, Any]],
    results: list[dict[str, Any]],
    terms: tuple[str, ...],
    org: str,
    date: str,
) -> None:
    with output_path.open("w", encoding="utf-8") as handle:
        handle.write("# Public Jupiter Repository Crawl\n\n")
        handle.write(f"Date: {date}\n\n")
        handle.write(f"Organisation: `{org}`\n\n")
        handle.write("Search terms:\n\n")
        for term in terms:
            handle.write(f"- `{term}`\n")
        handle.write("\n## Summary\n\n")
        handle.write(f"- Public repositories enumerated: {len(repos)}\n")
        handle.write(f"- Repositories scanned: {sum(1 for r in results if r['status'] == 'scanned')}\n")
        handle.write(f"- Repositories with hits: {sum(1 for r in results if r.get('term_counts'))}\n")
        handle.write(f"- Repositories skipped or failed: {sum(1 for r in results if r['status'] != 'scanned')}\n\n")

        handle.write("## Repositories With Hits\n\n")
        hit_results = [result for result in results if result.get("term_counts")]
        if not hit_results:
            handle.write("No target-term hits were found.\n\n")
        else:
            handle.write("| Repository | Terms | First observed hits |\n")
            handle.write("|---|---|---|\n")
            for result in hit_results:
                terms_text = ", ".join(
                    f"`{term}` {count}" for term, count in sorted(result["term_counts"].items())
                )
                first_hits = "<br>".join(
                    f"`{hit['path']}:{hit['line']}` {', '.join(hit['terms'])}: {hit['snippet']}"
                    for hit in result["hits"][:5]
                )
                handle.write(f"| `{result['full_name']}` | {terms_text} | {first_hits} |\n")
            handle.write("\n")

        failed = [result for result in results if result["status"] != "scanned"]
        if failed:
            handle.write("## Failed Or Skipped Repositories\n\n")
            handle.write("| Repository | Status | Error |\n")
            handle.write("|---|---|---|\n")
            for result in failed:
                error = result.get("error", "").replace("|", "\\|")
                handle.write(f"| `{result['full_name']}` | {result['status']} | {error[:300]} |\n")
            handle.write("\n")

        handle.write("## Interpretation\n\n")
        handle.write(
            "This crawl is a public-source clue finder. Hits are not utility evidence by themselves. "
            "A useful hit must connect JUP to validator/Dove security, signer weights, quorum, fees, "
            "governance, access control, slashing, rewards or a permanent protocol sink.\n"
        )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--org", default="jup-ag")
    parser.add_argument("--output-dir", default="research")
    parser.add_argument("--work-dir", default=None)
    parser.add_argument("--max-repos", type=int, default=0)
    parser.add_argument("--max-file-bytes", type=int, default=1_000_000)
    parser.add_argument("--terms", nargs="*", default=list(DEFAULT_TERMS))
    args = parser.parse_args()

    terms = tuple(term.lower() for term in args.terms)
    date = dt.date.today().isoformat()
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    repos = fetch_public_repos(args.org)
    if args.max_repos:
        repos = repos[: args.max_repos]

    work_root = Path(args.work_dir) if args.work_dir else Path(tempfile.mkdtemp(prefix="jup-ag-crawl-"))
    work_root.mkdir(parents=True, exist_ok=True)

    results: list[dict[str, Any]] = []
    try:
        for index, repo in enumerate(repos, start=1):
            repo_dir = work_root / repo["full_name"].replace("/", "__")
            if repo_dir.exists():
                shutil.rmtree(repo_dir)
            print(f"[{index}/{len(repos)}] {repo['full_name']}", flush=True)
            cloned, error = clone_repo(repo, repo_dir)
            if not cloned:
                results.append(
                    {
                        "full_name": repo["full_name"],
                        "html_url": repo["html_url"],
                        "status": "clone_failed",
                        "error": error,
                    }
                )
                continue

            results.append(
                {
                    "full_name": repo["full_name"],
                    "html_url": repo["html_url"],
                    "description": repo.get("description"),
                    "status": "scanned",
                    **scan_repo(repo_dir, terms, args.max_file_bytes),
                }
            )

        json_path = output_dir / f"jup-ag-public-repo-crawl-{date}.json"
        md_path = output_dir / f"jup-ag-public-repo-crawl-{date}.md"
        json_path.write_text(json.dumps(results, indent=2, sort_keys=True), encoding="utf-8")
        write_markdown(md_path, repos, results, terms, args.org, date)
        print(f"Wrote {md_path}")
        print(f"Wrote {json_path}")
    finally:
        if args.work_dir is None:
            shutil.rmtree(work_root, ignore_errors=True)

    return 0


if __name__ == "__main__":
    sys.exit(main())
