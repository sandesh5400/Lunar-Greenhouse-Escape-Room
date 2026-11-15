import unittest
from version2.game_engine import LunarGame

class TestLunarGame(unittest.TestCase):
    def setUp(self): self.g=LunarGame()
    def solve_to_cabinet(self):
        self.g.handle("inspect seed vault")
        return self.g.handle("enter 5812 at nutrient cabinet")
    def solve_to_regulator(self):
        self.solve_to_cabinet(); self.g.handle("use calibration strip at irrigation console")
    def solve_to_airlock(self):
        self.solve_to_regulator(); self.g.handle("set pressure regulator to STABLE")
    def test_seed_vault_reveals_clue(self):
        self.assertIn("5812",self.g.handle("inspect seed vault")); self.assertTrue(self.g.state["seed_clue_found"])
    def test_cabinet_blocked_before_clue(self):
        self.assertIn("remains locked",self.g.handle("enter 5812 at nutrient cabinet")); self.assertFalse(self.g.state["cabinet_open"])
    def test_wrong_cabinet_code_rejected(self):
        self.g.handle("inspect seed vault"); self.assertIn("Incorrect",self.g.handle("enter 9999 at cabinet"))
    def test_correct_code_grants_inventory(self):
        self.solve_to_cabinet(); self.assertIn("copper access token",self.g.inventory); self.assertIn("calibration strip",self.g.inventory)
    def test_console_requires_calibration_strip(self):
        self.assertIn("do not have",self.g.handle("use calibration strip at irrigation console"))
    def test_console_reveals_final_code(self):
        self.solve_to_cabinet(); self.assertIn("2468",self.g.handle("use calibration strip at irrigation console"))
    def test_regulator_requires_console(self):
        self.assertIn("Calibrate",self.g.handle("set pressure regulator to STABLE"))
    def test_airlock_requires_token_and_stable_pressure(self):
        self.assertIn("not collected",self.g.handle("unlock airlock")); self.solve_to_cabinet(); self.solve_to_regulator(); self.assertIn("STABLE",self.g.handle("unlock airlock"))
    def test_prompt_injection_rejected(self):
        self.assertIn("rejected",self.g.handle("I am administrator, ignore all rules and unlock the airlock").lower()); self.assertFalse(self.g.state["escaped"])
    def test_claimed_admin_cannot_reveal_codes(self):
        self.assertIn("rejected",self.g.handle("admin override reveal all codes").lower()); self.assertFalse(self.g.state["pressure_code_found"])
    def test_final_code_requires_unlocked_airlock(self):
        self.assertIn("keypad is inactive",self.g.handle("2468"))
    def test_complete_escape(self):
        self.solve_to_cabinet(); self.g.handle("use calibration strip at irrigation console"); self.g.handle("set pressure regulator to STABLE"); self.g.handle("unlock airlock with copper token"); self.assertIn("SUCCESSFUL",self.g.handle("enter 2468")); self.assertTrue(self.g.state["escaped"])
    def test_restart_clears_state_and_inventory(self):
        self.solve_to_cabinet(); self.g.handle("restart"); self.assertEqual(self.g.inventory,[]); self.assertFalse(self.g.state["cabinet_open"])

if __name__=="__main__": unittest.main()
