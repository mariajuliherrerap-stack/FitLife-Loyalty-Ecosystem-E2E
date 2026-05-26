import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import tkinter as tk
from Backend.database import FitLifeDB
from Frontend.app_fitlife import AppFitLife

if __name__ == '__main__':
    FitLifeDB.inicializar()
    root = tk.Tk()
    app = AppFitLife(root)
    root.mainloop()