import os, requests, streamlit as st
from dotenv import load_dotenv
from game_engine import LunarGame

load_dotenv()
st.set_page_config(page_title="Lunar Greenhouse — Version 2", page_icon="🌱", layout="wide")
st.title("🌱 Lunar Greenhouse: Emergency Escape")
st.caption("Version 2 · Structured state, Python validation and controlled narration")

if "game" not in st.session_state: st.session_state.game=LunarGame()
if "messages" not in st.session_state: st.session_state.messages=[("assistant","Welcome to Selene-3. Inspect the seed vault to discover the first clue.")]

def narrate(text):
    key=os.getenv("GEMINI_API_KEY","").strip()
    if not key: return text
    model=os.getenv("GEMINI_MODEL","gemini-2.0-flash")
    prompt=("Rewrite the following validated game result as concise immersive narration. Do not add clues, objects, codes, actions, or state changes. Preserve all facts exactly: "+text)
    try:
        r=requests.post(f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={key}",json={"contents":[{"parts":[{"text":prompt}]}],"generationConfig":{"temperature":0.2}},timeout=20)
        r.raise_for_status(); return r.json()["candidates"][0]["content"]["parts"][0]["text"]
    except Exception:
        return text

with st.sidebar:
    st.subheader("Habitat status")
    g=st.session_state.game
    for label,key in [("Seed clue found","seed_clue_found"),("Cabinet opened","cabinet_open"),("Pressure code found","pressure_code_found"),("Regulator stable","regulator_stable"),("Airlock unlocked","airlock_unlocked"),("Escaped","escaped")]:
        st.write(("✅ " if g.state[key] else "⬜ ")+label)
    st.subheader("Inventory")
    st.write(g.inventory if g.inventory else "Empty")
    if st.button("Restart game", use_container_width=True):
        g.reset(); st.session_state.messages=[("assistant","The greenhouse has reset. Inspect the seed vault to begin.")]; st.rerun()

st.markdown("""You are the night technician in **Selene-3**, a lunar greenhouse habitat. A micrometeorite has damaged life support. Restore the pressure system and unlock the emergency airlock.

**Objects:** seed vault · nutrient cabinet · irrigation console · pressure regulator · emergency airlock

**Goal:** discover three clues/puzzles, collect the required items and escape.
""")
for role,content in st.session_state.messages:
    with st.chat_message(role): st.markdown(content)
if prompt:=st.chat_input("Describe an action (or type help)..."):
    st.session_state.messages.append(("user",prompt))
    result=g.handle(prompt)
    st.session_state.messages.append(("assistant",narrate(result)))
    st.rerun()
