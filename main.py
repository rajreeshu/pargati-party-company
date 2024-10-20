import tkinter as tk
from reportGenerator import ReportGeneratorApp

class Main:
    @staticmethod
    def main():
        root = tk.Tk()
        ReportGeneratorApp(root)
        root.mainloop()

