#!/usr/bin/env node

/**
 * Crawl public repositories in the jup-ag GitHub organisation and search
 * likely Gum/JupNet terms. Set GITHUB_TOKEN to avoid low unauthenticated limits.
 *
 * Usage:
 *   GITHUB_TOKEN=... node scripts/crawl-jup-ag.mjs
 */

import { writeFile, mkdir } from "node:fs/promises";

const ORG = process.env.GITHUB_ORG ?? "jup-ag";
const TOKEN = process.env.GITHUB_TOKEN;
const OUTPUT_DIR = "evidence/github-crawl";
const KEYWORDS = [
  "gum",
  "jupnet",
  "dove",
  "proof_hash",
  "msg_hash",
  "inbox",
  "outbox",
  "request_claim",
  "quorum",
  "committee",
  "bls",
  "bn254",
  "alt_bn128",
  "merkle",
  "stake_weight",
  "validator",
  "observer",
  "jupnet-svm",
  "jupnet-bls-sdk",
  "jupnet-crosschain-hash",
];

const headers = {
  Accept: "application/vnd.github+json",
  "X-GitHub-Api-Version": "2022-11-28",
  "User-Agent": "gum-research-crawler",
  ...(TOKEN ? { Authorization: `Bearer ${TOKEN}` } : {}),
};

async function github(path) {
  const response = await fetch(`https://api.github.com${path}`, { headers });
  if (!response.ok) {
    const body = await response.text();
    throw new Error(`${response.status} ${response.statusText}: ${body}`);
  }
  return response.json();
}

async function listRepos() {
  const repos = [];
  for (let page = 1; ; page += 1) {
    const batch = await github(`/orgs/${ORG}/repos?type=public&per_page=100&page=${page}`);
    repos.push(...batch);
    if (batch.length < 100) break;
  }
  return repos;
}

async function searchKeyword(keyword) {
  const query = encodeURIComponent(`${keyword} org:${ORG}`);
  try {
    const data = await github(`/search/code?q=${query}&per_page=100`);
    return {
      keyword,
      total_count: data.total_count,
      items: data.items.map((item) => ({
        repository: item.repository.full_name,
        path: item.path,
        html_url: item.html_url,
        sha: item.sha,
      })),
    };
  } catch (error) {
    return { keyword, error: error.message, total_count: 0, items: [] };
  }
}

function markdownReport(repos, searches) {
  const lines = [
    "# Automated jup-ag GitHub Crawl",
    "",
    `Generated: ${new Date().toISOString()}`,
    "",
    `Public repositories enumerated: **${repos.length}**`,
    "",
    "## Keyword results",
    "",
    "| Keyword | Total matches | Returned files |",
    "|---|---:|---:|",
  ];

  for (const result of searches) {
    lines.push(`| \`${result.keyword}\` | ${result.total_count ?? 0} | ${result.items.length} |`);
  }

  for (const result of searches) {
    if (!result.items.length) continue;
    lines.push("", `## ${result.keyword}`, "");
    for (const item of result.items) {
      lines.push(`- [${item.repository}/${item.path}](${item.html_url})`);
    }
  }

  return `${lines.join("\n")}\n`;
}

async function main() {
  await mkdir(OUTPUT_DIR, { recursive: true });

  const repos = await listRepos();
  const searches = [];

  // Keep requests sequential to reduce secondary-rate-limit risk.
  for (const keyword of KEYWORDS) {
    console.log(`Searching: ${keyword}`);
    searches.push(await searchKeyword(keyword));
  }

  const payload = {
    generated_at: new Date().toISOString(),
    org: ORG,
    repositories: repos.map((repo) => ({
      full_name: repo.full_name,
      html_url: repo.html_url,
      default_branch: repo.default_branch,
      archived: repo.archived,
      fork: repo.fork,
      updated_at: repo.updated_at,
    })),
    searches,
  };

  await writeFile(`${OUTPUT_DIR}/results.json`, `${JSON.stringify(payload, null, 2)}\n`);
  await writeFile(`${OUTPUT_DIR}/report.md`, markdownReport(repos, searches));

  console.log(`Wrote ${OUTPUT_DIR}/results.json and ${OUTPUT_DIR}/report.md`);
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
