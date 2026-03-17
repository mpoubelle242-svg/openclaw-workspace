#!/usr/bin/env python3
"""Optimize agent models: only OpenRouter, prioritize hunter-alpha, healer-alpha, and :free models."""
import json
from pathlib import Path

AGENTS_DIR = Path("/root/.openclaw/agents")
CONFIG_PATH = Path("/root/.openclaw/openclaw.json")

PRIORITIZED = ["openrouter/hunter-alpha", "openrouter/healer-alpha"]

def load_global_allowed():
    with open(CONFIG_PATH, "r") as f:
        config = json.load(f)
    fallbacks = config["agents"]["defaults"]["model"]["fallbacks"]
    allowed = []
    for model_id in fallbacks:
        if model_id in PRIORITIZED:
            allowed.append(model_id)
        elif model_id.startswith("openrouter/") and model_id.endswith(":free"):
            allowed.append(model_id)
    # Ensure prioritized are first
    ordered = []
    for p in PRIORITIZED:
        if p in allowed:
            ordered.append(p)
            allowed.remove(p)
    # sort remaining alphabetically
    allowed.sort()
    ordered.extend(allowed)
    return ordered

def build_model_entry(model_id):
    # We can add alias if needed, but skip for now
    return {"id": model_id}

def update_models_file(path, allowed_models):
    with open(path, "r") as f:
        data = json.load(f)
    
    openrouter = data.get("providers", {}).get("openrouter")
    if not openrouter:
        return False
    
    models = openrouter.get("models", [])
    new_models = [build_model_entry(mid) for mid in allowed_models]
    if models == new_models:
        return False
    
    openrouter["models"] = new_models
    with open(path, "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    return True

def main():
    allowed = load_global_allowed()
    print(f"Allowed models: {allowed}")
    
    updated = []
    for agent_dir in AGENTS_DIR.iterdir():
        models_path = agent_dir / "agent" / "models.json"
        if not models_path.exists():
            continue
        if update_models_file(models_path, allowed):
            updated.append(agent_dir.name)
            print(f"Updated {agent_dir.name}")
    
    print(f"Total updated: {len(updated)}")

if __name__ == "__main__":
    main()