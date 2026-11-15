# Lunar Greenhouse: Emergency Escape

An AI-powered escape-room prototype set inside **Selene-3**, a lunar greenhouse habitat. The player investigates damaged life-support equipment, solves linked puzzles, collects items and opens the emergency airlock.

## Versions
- **Version 1:** Streamlit chat interface with an LLM-led Game Master. Gemini is optional; a local scripted Game Master is available without an API key.
- **Version 2:** Streamlit interface backed by a Python game engine. Structured state, inventory, puzzle prerequisites and action validation remain outside the LLM. Optional narration cannot change validated game outcomes.

## Requirements
- Windows 10/11
- Python 3.11+ (Python 3.14 may work if compatible wheels are available)
- Internet connection for dependency installation and optional Gemini API

## Windows setup

```powershell
py -3 -m venv .venv
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
Copy-Item .env.example .env
```

## Run Version 2

```powershell
streamlit run version2/app.py
```
Open http://localhost:8501.

## Run Version 1

In a second PowerShell window, from the project directory:

```powershell
.\.venv\Scripts\Activate.ps1
streamlit run version1/app.py --server.port 8502
```
Open http://localhost:8502.

## Optional Gemini API

Add a valid key to your local `.env` file:

```env
GEMINI_API_KEY=YOUR_API_KEY_HERE
GEMINI_MODEL=gemini-2.0-flash
```

The project does not require a paid API. Without a key, Version 1 uses its local scripted Game Master and Version 2 uses deterministic Python results.

## Puzzle path

| Stage | Action | Outcome |
|---|---|---|
| 1 | Inspect seed vault | Reveals 5812 |
| 2 | Enter 5812 at nutrient cabinet | Collect copper access token and calibration strip |
| 3 | Use calibration strip at irrigation console | Reveals 2468 |
| 4 | Set pressure regulator to STABLE | Airlock pressure normalized |
| 5 | Unlock airlock with copper token | Keypad activated |
| 6 | Enter 2468 | Escape successful |

## Tests

From the repository root:

```powershell
python -m unittest discover -s tests -v
```

Test cases cover clue discovery, locked prerequisites, wrong codes, inventory, console access, regulator state, airlock access, prompt injection, premature final code, successful escape and restart.

## Repository layout

```text
Lunar-Greenhouse-Escape-Room/
├── version1/app.py
├── version2/app.py
├── version2/game_engine.py
├── tests/test_game_engine.py
├── figures/architecture_v1.png
├── figures/architecture_v2.png
├── data/test_matrix.csv
├── docs/technical_summary.docx
├── docs/technical_summary.md
├── README.md
├── requirements.txt
├── .env.example
└── .gitignore
```

## Limitations

Version 2 uses deterministic intent patterns and aliases rather than unrestricted natural-language understanding. This keeps state transitions auditable and prevents the LLM from authorizing puzzle completion. Version 1 is intentionally more flexible and less robust, consistent with the staged project brief.

## Author
Sandesh HP 
University of Europe for Applied Sciences
