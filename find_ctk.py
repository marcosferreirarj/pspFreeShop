import customtkinter
import os
ctk_path = os.path.dirname(customtkinter.__file__)
print(f"CTK_PATH={ctk_path}")
print(f"GUI_PATH={os.path.join(ctk_path, 'gui')}")
print(f"ASSETS_PATH={os.path.join(ctk_path, 'assets')}")
