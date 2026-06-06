"""Extract Claude Code session data from ~/.claude/projects/ into data/extracted/claude_code/."""

import json
from pathlib import Path

CLAUDE_PROJECTS = Path.home() / ".claude" / "projects"
OUT_DIR = Path(__file__).parent.parent / "data" / "extracted" / "claude_code"


def project_name_from_folder(folder_name: str) -> str:
    """Convert '-Users-aebel-foo-bar' -> 'foo/bar'."""
    parts = folder_name.lstrip("-").split("-")
    # drop 'Users' and username
    try:
        users_idx = next(i for i, p in enumerate(parts) if p == "Users")
        parts = parts[users_idx + 2 :]
    except StopIteration:
        pass
    return "/".join(parts)


def extract_text(content) -> str:
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        return " ".join(
            block.get("text", "")
            for block in content
            if isinstance(block, dict) and block.get("type") == "text"
        )
    return ""


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    out_path = OUT_DIR / "messages.jsonl"

    total = 0
    with open(out_path, "w") as out_f:
        for project_dir in sorted(CLAUDE_PROJECTS.iterdir()):
            if not project_dir.is_dir():
                continue
            project = project_name_from_folder(project_dir.name)

            for jsonl_file in sorted(project_dir.glob("*.jsonl")):
                session_id = jsonl_file.stem
                with open(jsonl_file) as f:
                    for line in f:
                        line = line.strip()
                        if not line:
                            continue
                        try:
                            obj = json.loads(line)
                        except json.JSONDecodeError:
                            continue

                        msg_type = obj.get("type")
                        if msg_type not in ("user", "assistant"):
                            continue

                        message = obj.get("message", {})
                        usage = message.get("usage", {})

                        record = {
                            "message_id": obj.get("uuid"),
                            "parent_message_id": obj.get("parentUuid"),
                            "session_id": obj.get("sessionId", session_id),
                            "role": msg_type,
                            "timestamp": obj.get("timestamp"),
                            "text": extract_text(message.get("content", "")),
                            "project": project,
                            "cwd": obj.get("cwd"),
                            "git_branch": obj.get("gitBranch"),
                            "version": obj.get("version"),
                            "model": message.get("model"),
                            "input_tokens": usage.get("input_tokens"),
                            "output_tokens": usage.get("output_tokens"),
                            "cache_read_tokens": usage.get("cache_read_input_tokens"),
                            "cache_creation_tokens": usage.get("cache_creation_input_tokens"),
                        }
                        out_f.write(json.dumps(record) + "\n")
                        total += 1

    print(f"Wrote {total} messages to {out_path}")


if __name__ == "__main__":
    main()
