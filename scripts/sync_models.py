#!/usr/bin/env python3
"""Synchronise per-agent model lists/fallbacks with the global OpenClaw config."""
import json
import subprocess
from pathlib import Path
from datetime import datetime, timezone

CONFIG_ROOT = Path("/root/.openclaw")
AGENTS_DIR = CONFIG_ROOT / "agents"
SCRIPT_NAME = "sync-models"


def run(cmd):
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"Command failed ({' '.join(cmd)}): {result.stderr.strip()}")
    return result.stdout.strip()


def config_get(path):
    output = run(["openclaw", "config", "get", path])
    return json.loads(output)


def load_models_file(agent_id):
    models_path = AGENTS_DIR / agent_id / "agent" / "models.json"
    if not models_path.exists():
        return None, None
    with models_path.open("r", encoding="utf-8") as fh:
        data = json.load(fh)
    return data, models_path


def save_models_file(path, data):
    tmp_path = path.with_suffix(".tmp")
    with tmp_path.open("w", encoding="utf-8") as fh:
        json.dump(data, fh, indent=2, ensure_ascii=False)
        fh.write("\n")
    tmp_path.replace(path)


def build_model_entry(model_id, meta):
    entry = {"id": model_id}
    if isinstance(meta, dict):
        entry.update(meta)
    return entry


def normalize_model_info(model_info):
    """Convert model info to dict with primary and fallbacks."""
    if isinstance(model_info, str):
        return {"primary": model_info, "fallbacks": []}
    elif isinstance(model_info, dict):
        if "fallbacks" not in model_info:
            model_info["fallbacks"] = []
        return model_info
    else:
        return {"primary": "", "fallbacks": []}


def main():
    timestamp = datetime.now(timezone.utc).isoformat()
    print(f"[{SCRIPT_NAME}] {timestamp} — Starting sync")

    global_model = config_get("agents.defaults.model")
    global_models_meta = config_get("agents.defaults.models")
    global_fallbacks = global_model.get("fallbacks", [])

    updated_files = []
    for agent_dir in AGENTS_DIR.iterdir():
        if not agent_dir.is_dir():
            continue
        agent_id = agent_dir.name
        data, models_path = load_models_file(agent_id)
        if data is None or models_path is None:
            continue
        providers = data.get("providers", {})
        openrouter = providers.get("openrouter")
        if not isinstance(openrouter, dict):
            continue
        existing_models = openrouter.get("models", [])
        new_models = [build_model_entry(mid, global_models_meta.get(mid)) for mid in global_fallbacks]
        if existing_models == new_models:
            continue
        openrouter["models"] = new_models
        save_models_file(models_path, data)
        updated_files.append(agent_id)
        print(f"[{SCRIPT_NAME}] Updated models.json for agent '{agent_id}'")

    if not updated_files:
        print(f"[{SCRIPT_NAME}] No changes required — already in sync")
    else:
        print(f"[{SCRIPT_NAME}] Sync complete. Files updated: {updated_files}")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"[{SCRIPT_NAME}] ERROR: {exc}")
        raise
