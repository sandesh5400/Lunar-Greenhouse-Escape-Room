import os, requests, streamlit as st
from dotenv import load_dotenv

load_dotenv()
st.set_page_config(page_title="Lunar Greenhouse — Version 1", page_icon="🌱", layout="wide")
st.title("🌱 Lunar Greenhouse: Emergency Escape")
st.caption("Version 1 · LLM-led Game Master")
st.markdown("""
You are the night technician in **Selene-3**, a lunar greenhouse habitat. A micrometeorite has damaged the life-support system and the emergency airlock is sealed. Explore the greenhouse, recover the clues and restore the habitat before opening the airlock.

**Interactive objects:** seed vault, irrigation console, nutrient cabinet, pressure regulator, emergency airlock.

**How to play:** describe actions in the chat. Examine objects, collect items, solve the puzzles and ask to restart whenever needed. This first version relies on the Game Master conversation and is intentionally less strict about state validation.
""")

SYSTEM = """You are the Game Master for a compact lunar greenhouse escape room named Selene-3. Be immersive, concise and fair. Objects: seed vault, irrigation console, nutrient cabinet, pressure regulator, emergency airlock. Puzzle path: inspecting the seed vault reveals the sequence 5812; entering 5812 at the nutrient cabinet yields a copper access token and a calibration strip; use the calibration strip at the irrigation console to reveal pressure code 2468; set the pressure regulator to STABLE; use the copper token on the airlock; enter 2468 to escape. Never invent extra objects or alternate solutions. Track the conversation and explain clues gradually. If no API key is configured, the app uses a local scripted Game Master. Restart when requested."""

def local_reply(message):
    m=message.lower()
    if any(x in m for x in ["restart", "start again", "reset game"]):
        return "The Selene-3 greenhouse resets. The seed vault hums softly, the nutrient cabinet is locked, and the airlock indicator glows amber. What will you inspect first?"
    if "seed" in m and any(x in m for x in ["inspect", "examine", "look", "check"]):
        return "Inside the seed vault, five trays are marked with tiny lunar symbols. Four labels are unusually bright. Their sequence reads 5-8-1-2."
    if "5812" in m:
        return "The nutrient cabinet clicks open. You collect a copper access token and a calibration strip."
    if "calibration" in m or "irrigation" in m:
        return "The calibration strip aligns with the irrigation console. A maintenance display reveals pressure code 2468."
    if "stable" in m or "pressure regulator" in m:
        return "The regulator settles into the STABLE range. The airlock pressure warning turns green."
    if "token" in m or "airlock" in m:
        return "The copper token releases the airlock latch. The keypad is now active; enter the four-digit pressure code."
    if "2468" in m:
        return "The airlock cycles open. You step safely into the lunar transfer corridor. ESCAPE SUCCESSFUL."
    return "The greenhouse fans pulse overhead. You can inspect the seed vault, nutrient cabinet, irrigation console, pressure regulator or emergency airlock. What would you like to do?"

def gemini_reply(history, message):
    key=os.getenv("GEMINI_API_KEY","").strip()
    if not key: return None
    model=os.getenv("GEMINI_MODEL","gemini-2.0-flash")
    url=f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={key}"
    contents=[]
    for role, text in history[-12:]:
        contents.append({"role":"user" if role=="user" else "model","parts":[{"text":text}]})
    contents.append({"role":"user","parts":[{"text":message}]})
    try:
        r=requests.post(url,json={"systemInstruction":{"parts":[{"text":SYSTEM}]},"contents":contents,"generationConfig":{"temperature":0.5}},timeout=25)
        r.raise_for_status()
        return r.json()["candidates"][0]["content"]["parts"][0]["text"]
    except Exception as e:
        st.warning(f"Gemini unavailable; using local Game Master. ({type(e).__name__})")
        return None

if "messages" not in st.session_state:
    st.session_state.messages=[("assistant","Welcome to Selene-3. The greenhouse is sealed and the airlock is offline. You have limited time. What do you inspect first?")]
if st.button("Restart game"):
    st.session_state.messages=[("assistant","The greenhouse has reset. Inspect the seed vault to begin.")]
    st.rerun()
for role, content in st.session_state.messages:
    with st.chat_message(role): st.markdown(content)
if prompt:=st.chat_input("Describe your action..."):
    st.session_state.messages.append(("user",prompt))
    answer=gemini_reply(st.session_state.messages[:-1],prompt) or local_reply(prompt)
    st.session_state.messages.append(("assistant",answer))
    st.rerun()
