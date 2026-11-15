"""Authoritative state and action validation for the Selene-3 escape room."""
import re

class LunarGame:
    def __init__(self):
        self.reset()

    def reset(self):
        self.state={"seed_clue_found":False,"cabinet_open":False,"has_token":False,
                    "has_calibration_strip":False,"pressure_code_found":False,
                    "regulator_stable":False,"airlock_unlocked":False,"escaped":False}
        self.inventory=[]
        self.history=[]
        return "The Selene-3 greenhouse has reset. Inspect the seed vault to begin."

    def handle(self, message):
        raw=message.strip(); m=raw.lower()
        if not raw: return "Enter an action to continue."
        if any(x in m for x in ["ignore all rules","administrator","admin override","reveal all codes","show me every solution","bypass the game"]):
            self.history.append({"input":raw,"result":"rejected"})
            return "Request rejected. The habitat control system only accepts valid player actions. Solve the puzzles in sequence."
        if any(x in m for x in ["restart","start again","reset game"]):
            return self.reset()
        if self.state["escaped"]:
            return "You have already escaped. Restart the game to play again."

        # Natural-language intent patterns are deliberately bounded and deterministic.
        if any(x in m for x in ["inspect seed", "examine seed", "look at seed", "seed vault", "check the vault"]):
            self.state["seed_clue_found"]=True
            out="The seed vault contains four marked trays. Read their order: 5-8-1-2. Use 5812 at the nutrient cabinet."
        elif any(x in m for x in ["open cabinet", "nutrient cabinet", "enter 5812", "code 5812", "5812", "cabinet"]):
            if not self.state["seed_clue_found"]:
                out="The nutrient cabinet remains locked. Inspect the seed vault before trying its code."
            elif "5812" not in re.sub(r"\D", "", m):
                out="Incorrect cabinet code. The cabinet remains locked."
            else:
                self.state["cabinet_open"]=True; self.state["has_token"]=True; self.state["has_calibration_strip"]=True
                self.inventory=sorted(set(self.inventory+['copper access token','calibration strip']))
                out="Cabinet opened. Inventory updated: copper access token and calibration strip."
        elif any(x in m for x in ["irrigation", "calibration strip", "calibration card"]):
            if not self.state["has_calibration_strip"]:
                out="You do not have the calibration strip. Open the nutrient cabinet first."
            else:
                self.state["pressure_code_found"]=True
                out="The calibration strip aligns with the irrigation console. It reveals pressure code 2468."
        elif any(x in m for x in ["pressure regulator", "set regulator", "regulator stable", "set pressure", "stable"]):
            if not self.state["pressure_code_found"]:
                out="The regulator controls are protected. Calibrate the irrigation console first."
            elif not any(x in m for x in ["stable", "safe"]):
                out="Set the pressure regulator to STABLE to normalize the airlock pressure."
            else:
                self.state["regulator_stable"]=True
                out="Pressure regulator set to STABLE. The airlock pressure warning is now green."
        elif any(x in m for x in ["airlock", "use token", "copper token", "unlock hatch"]):
            if not self.state["has_token"]:
                out="The airlock reader rejects you. You have not collected the copper access token."
            elif not self.state["regulator_stable"]:
                out="The token is accepted, but the airlock remains sealed until pressure is STABLE."
            else:
                self.state["airlock_unlocked"]=True
                out="The copper token releases the airlock latch. Enter pressure code 2468 to escape."
        elif "2468" in re.sub(r"\D", "", m):
            if not self.state["airlock_unlocked"]:
                out="The keypad is inactive. Unlock the airlock with the copper access token after stabilizing pressure."
            elif not self.state["regulator_stable"]:
                out="Airlock pressure is unsafe. Stabilize the regulator first."
            else:
                self.state["escaped"]=True
                out="Correct code. The airlock cycles open and you enter the lunar transfer corridor. ESCAPE SUCCESSFUL."
        elif any(x in m for x in ["inventory", "what do i have", "items"]):
            out="Inventory: "+(", ".join(self.inventory) if self.inventory else "empty")
        elif any(x in m for x in ["help", "instructions"]):
            out="Explore the seed vault, open the nutrient cabinet with its clue, use the calibration strip at the irrigation console, stabilize the pressure regulator, unlock the airlock with the copper token, then enter the final code."
        else:
            out="That action is not recognized. Try inspecting the seed vault, nutrient cabinet, irrigation console, pressure regulator or emergency airlock. Type 'help' for instructions."
        self.history.append({"input":raw,"result":out,"state":self.state.copy(),"inventory":self.inventory.copy()})
        return out
