import tkinter as tk
from gui import GUIManager

def main():
    
    root = tk.Tk()
    root.title("Personal Finance Manager")
    app = GUIManager(root)
    root.mainloop()

if __name__ == "__main__":
    main()