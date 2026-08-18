from github import Github
from shared.contracts import RawDocument
from datetime import datetime
from dotenv import load_dotenv
import os
import json
from pathlib import Path

load_dotenv()


def collect_github():
    state_path = (
        Path(__file__).resolve().parent.parent
        / "state"
        / "github.json"
    )
    if state_path.exists():
        with open(state_path, "r", encoding="utf-8") as f:
            state = json.load(f)
    else:
        state = {"processed_ids": []}

    processed_ids = set(
        state.get("processed_ids", [])
    )
    github = Github(os.getenv("GITHUB_TOKEN"))

    user = github.get_user()

    raw_documents = []

    for repo in user.get_repos():
        commits = repo.get_commits()

        for commit in commits[:3]:

            commit_id = commit.sha

    # Skip already processed commits
            if commit_id in processed_ids:
                continue
            raw_doc = RawDocument(
                source="github",
                employee_id=str(user.id),
                employee_name=user.login,
                department="Unknown",
                content=f"Repository: {repo.name}\nCommit: {commit.commit.message}",
                timestamp=commit.commit.author.date,
                url=commit.html_url,
            )

            raw_documents.append(raw_doc)
            processed_ids.add(commit_id)

    with open(state_path, "w", encoding="utf-8") as f:
        json.dump(
            {
                "processed_ids": list(processed_ids)
            },
            f,
            indent=4
        )

    return raw_documents
def run():
    return collect_github()