from __future__ import annotations

import os
from typing import Optional


def push_text_file_to_github(
    owner_repo: str,
    file_path: str,
    content: str,
    commit_message: str,
    branch: str = "main",
    token: Optional[str] = None,
) -> str:
    """Create or update a text file in a GitHub repository via the Contents API."""
    if "/" not in owner_repo:
        raise ValueError("owner_repo must be in 'owner/repo' format")

    auth_token = token or os.getenv("GITHUB_TOKEN")
    if not auth_token:
        raise RuntimeError("GITHUB_TOKEN is not set")

    try:
        import requests  # type: ignore
    except Exception as exc:  # pragma: no cover
        raise RuntimeError("requests package is required for GitHub export") from exc

    owner, repo = owner_repo.split("/", 1)
    api = f"https://api.github.com/repos/{owner}/{repo}/contents/{file_path.lstrip('/')}"
    headers = {
        "Authorization": f"Bearer {auth_token}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }

    sha = None
    existing = requests.get(api, headers=headers, params={"ref": branch}, timeout=30)
    if existing.status_code == 200:
        data = existing.json()
        sha = data.get("sha")
    elif existing.status_code not in {404}:
        raise RuntimeError(f"GitHub lookup failed: {existing.status_code} {existing.text}")

    import base64

    payload = {
        "message": commit_message,
        "content": base64.b64encode(content.encode("utf-8")).decode("utf-8"),
        "branch": branch,
    }
    if sha:
        payload["sha"] = sha

    response = requests.put(api, headers=headers, json=payload, timeout=30)
    if response.status_code not in {200, 201}:
        raise RuntimeError(f"GitHub push failed: {response.status_code} {response.text}")

    result = response.json()
    return str(result.get("content", {}).get("html_url") or "")
