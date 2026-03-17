#!/usr/bin/env python3
"""Update openclaw.json config: optimize models, set primary/fallbacks per agent."""
import json
from pathlib import Path

CONFIG_PATH = Path("/root/.openclaw/openclaw.json")

PRIORITIZED = ["openrouter/hunter-alpha", "openrouter/healer-alpha"]

def load_allowed():
    with open(CONFIG_PATH, "r") as f:
        config = json.load(f)
    fallbacks = config["agents"]["defaults"]["model"]["fallbacks"]
    allowed = []
    for model_id in fallbacks:
        if model_id in PRIORITIZED:
            allowed.append(model_id)
        elif model_id.startswith("openrouter/") and model_id.endswith(":free"):
            allowed.append(model_id)
    ordered = []
    for p in PRIORITIZED:
        if p in allowed:
            ordered.append(p)
            allowed.remove(p)
    allowed.sort()
    ordered.extend(allowed)
    return ordered

def update_config():
    with open(CONFIG_PATH, "r") as f:
        config = json.load(f)
    
    allowed = load_allowed()
    print(f"Allowed models: {allowed}")
    
    # Update global defaults fallbacks
    config["agents"]["defaults"]["model"]["fallbacks"] = allowed
    # Update global models mapping (keep existing aliases)
    models_map = config["agents"]["defaults"]["models"]
    # Remove entries not in allowed
    to_remove = [k for k in models_map if k not in allowed]
    for k in to_remove:
        del models_map[k]
    # Ensure all allowed have an entry (empty object)
    for m in allowed:
        if m not in models_map:
            models_map[m] = {}
    
    # Define primary per agent
    primary_map = {
        "main": "openrouter/hunter-alpha",
        "whatsapp": "openrouter/healer-alpha",
        "research": "openrouter/healer-alpha",
        "files": "openrouter/hunter-alpha",
        "email": "openrouter/healer-alpha",
        "calendrier": "openrouter/hunter-alpha",
        "developpeur": "openrouter/hunter-alpha",
        "data-scientist": "openrouter/healer-alpha",
        "testeur": "openrouter/hunter-alpha",
        "chef-de-projet": "openrouter/hunter-alpha",
        "directeur-de-projet": "openrouter/healer-alpha",
    }
    
    # Update existing agents in list
    agents_list = config["agents"]["list"]
    for agent in agents_list:
        agent_id = agent["id"]
        primary = primary_map.get(agent_id, "openrouter/hunter-alpha")
        fallbacks = [m for m in allowed if m != primary]
        agent["model"] = {
            "primary": primary,
            "fallbacks": fallbacks
        }
        print(f"Updated agent {agent_id}: primary={primary}, {len(fallbacks)} fallbacks")
    
    # Add missing agents (chef-de-projet, data-scientist, testeur, directeur-de-projet)
    missing_agents = [
        {"id": "chef-de-projet", "name": "Chef de Projet", "model": {"primary": "openrouter/hunter-alpha", "fallbacks": [m for m in allowed if m != "openrouter/hunter-alpha"]}, "tools": {"profile": "full"}},
        {"id": "data-scientist", "name": "Data Scientist", "model": {"primary": "openrouter/healer-alpha", "fallbacks": [m for m in allowed if m != "openrouter/healer-alpha"]}, "tools": {"profile": "full"}},
        {"id": "testeur", "name": "Testeur", "model": {"primary": "openrouter/hunter-alpha", "fallbacks": [m for m in allowed if m != "openrouter/hunter-alpha"]}, "tools": {"profile": "full"}},
        {"id": "directeur-de-projet", "name": "Directeur de Projet", "model": {"primary": "openrouter/healer-alpha", "fallbacks": [m for m in allowed if m != "openrouter/healer-alpha"]}, "tools": {"profile": "full"}},
    ]
    for new_agent in missing_agents:
        if not any(a["id"] == new_agent["id"] for a in agents_list):
            agents_list.append(new_agent)
            print(f"Added agent {new_agent['id']}")
    
    # Write back
    with open(CONFIG_PATH, "w") as f:
        json.dump(config, f, indent=2, ensure_ascii=False)
    print("Config updated.")

if __name__ == "__main__":
    update_config()