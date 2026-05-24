# Thalexa OS

Personal AI Operating System scaffold generated from `Thalexa OS.MD`.

## Quick Start

1. Create a Python virtual environment:
   ```bash
   python -m venv venv
   .\venv\Scripts\activate
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   playwright install
   ```
3. Run the starter app:
   ```bash
   python main.py
   ```

## Project Structure

- `core/` — brain, models, agents, planner, memory, personality
- `voice/` — voice system runtime and wake word support
- `skills/` — skill categories for the Buddy OS
- `config/` — identity, personality, and model YAML configs
- `models/` — local GGUF and embedding model storage
- `vector_db/` — persistent memory store path
- `logs/` — runtime logs
- `scripts/` — environment and model checks

## Phase checklist

1. **Local model runtime**
   - `config/models.yaml` defines expected GGUF and embedding model paths
   - `core/models/model_manager.py` checks model availability and prints download instructions

2. **Voice system**
   - `core/voice/voice_manager.py` verifies runtime dependencies and placeholder flow
   - `main.py` now initializes voice and orchestrator components

3. **Memory system**
   - `core/memory/memory_store.py` ensures the `vector_db/` store exists
   - future work: add semantic memory and Chroma storage adapters

4. **Multi-agent system**
   - `core/agents/orchestrator.py` and `core/agents/memory_agent.py` provide starter agent scaffolding

## Setup helper

Run the setup check:
```bash
python scripts/setup_thalexa.py
```

## Notes

This scaffold is built from the AI Buddy OS plan in `Thalexa OS.MD` and the attached phase roadmap.
