# app/models/__init__.py
import os
import importlib

for filename in os.listdir(os.path.dirname(__file__)):
    if filename.endswith(".py") and filename not in ["__init__.py"]:
        module_name = f"{__name__}.{filename[:-3]}"
        importlib.import_module(module_name)
