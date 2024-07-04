import os
import sys
chemin_parent = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(chemin_parent)

from ui.interface import Interface

if __name__ == "__main__":
    inter = Interface()
    inter(True)