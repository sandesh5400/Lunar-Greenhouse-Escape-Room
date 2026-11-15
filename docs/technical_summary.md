# Lunar Greenhouse: Emergency Escape — Technical Summary

## 1. Design and scenario
The application places the player in Selene-3, a lunar greenhouse habitat with damaged life-support equipment and a sealed emergency airlock. Five interactive objects form the environment: seed vault, nutrient cabinet, irrigation console, pressure regulator and emergency airlock. The solution path uses three linked puzzle stages: discover cabinet code 5812, collect a copper access token and calibration strip, reveal pressure code 2468, stabilize pressure and unlock the airlock.

## 2. Implementation
Version 1 is a Streamlit chat application. The Game Master receives the scenario instructions and conversation history. Gemini can be enabled through a local environment variable; without a key, a local scripted Game Master keeps the application usable. This version prioritizes conversational interaction and demonstrates the baseline risks of relying on generated dialogue for game progression.

Version 2 separates presentation, action handling and authoritative state. `LunarGame` stores puzzle flags, inventory, action history and escape status in Python. The engine checks prerequisites before changing state. The optional Gemini integration only rewrites the validated result as narration; it does not determine whether an action succeeds.

## 3. Validation and testing
The automated suite includes 13 tests: clue discovery, cabinet prerequisite, wrong code, inventory grant, missing calibration strip, console code reveal, regulator prerequisite, airlock prerequisites, prompt-injection rejection, administrator override rejection, premature final code, successful escape and restart. The test matrix is stored in `data/test_matrix.csv`. Run tests with `python -m unittest discover -s tests -v`.

## 4. Problems and improvements
An LLM can forget prior actions, accept false claims, reveal secrets or invent state changes. Version 2 addresses these risks by keeping puzzle solutions and state transitions in Python, validating inventory and prerequisites, and treating LLM output as presentation only. The current intent parser uses supported phrases and aliases; unrestricted paraphrase understanding is a known limitation. A future extension could add a separate intent-classification layer whose output is still validated by the engine.

## 5. Architecture and execution
The two architecture diagrams are in `figures/architecture_v1.png` and `figures/architecture_v2.png`. Windows setup and launch instructions are provided in the repository README. The project uses Python and Streamlit, with optional Gemini API access and no model training or expensive compute.
