import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from pathlib import Path

from reportlab.lib.testutils import outputfile

from helpers import Helpers
from companyEnum import CompanyName
from data_processor import DataProcessor
from pdf_generator import PDFGenerator
from excel_loader import ExcelLoader
import os

class ReportGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Party-Company Report PDF Generator")
        self.root.geometry("400x400")  # Set a fixed size for the window

        self.file_path = None

        # Create main frame
        self.main_frame = tk.Frame(root, padx=10, pady=10)
        self.main_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        self.file_label = tk.Label(self.main_frame, text="No file selected" if self.file_path is None else Path(self.file_path).name, fg="green")

        self.file_label.pack(pady=10)

        # Create UI elements
        self.upload_button = tk.Button(self.main_frame, text="Upload Excel Report of Vyapar", command=self.upload_file, width=30)
        self.upload_button.pack(pady=10)

        # Add a dropdown for category selection
        self.category_label = tk.Label(self.main_frame, text="Select Category:")
        self.category_label.pack(pady=5)
        self.category_var = tk.StringVar()
        self.category_dropdown = ttk.Combobox(self.main_frame, textvariable=self.category_var)
        self.category_dropdown.pack(pady=10)
        self.category_dropdown['values'] = [category.value for category in CompanyName]  # Populate from enum
        self.category_dropdown.current(0)  # Set default value

        self.generate_button = tk.Button(self.main_frame, text="Generate PDF Report", command=self.generate_report, width=20)
        self.generate_button.pack(pady=10)

        self.status_label = tk.Label(self.main_frame, text="", fg="blue")
        self.status_label.pack(pady=10)

        # Add a progress bar
        self.progress_bar = ttk.Progressbar(self.main_frame, orient='horizontal', mode='determinate')
        self.progress_bar.pack(fill=tk.X, pady=10)

    def upload_file(self):
        # File dialog to select the Excel file
        self.file_path = filedialog.askopenfilename(
            filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")]
        )
        if self.file_path:
            file_name = Path(self.file_path).name
            self.file_label.config(text=f"File Selected: {file_name}")

    def generate_report(self):
        if not self.file_path:
            messagebox.showerror("Error", "Please upload an Excel file first.")
            return

        category = self.category_var.get()
        self.status_label.config(text=f"Generating report for category: {category}")

        try:
            # Extract the file name without extension for naming the PDF
            input_dir = Path(self.file_path).parent
            file_name = Path(self.file_path).stem
            
            # Load Excel data
            excel_loader = ExcelLoader(self.file_path)
            
            # Header data
            header_data = excel_loader.load_data("Party Statement Report", False)
            headerProcessor = DataProcessor(header_data)
            header_data = headerProcessor.getHeaderData(category)

            df = excel_loader.load_data('Item Details')

            if df is not None:
                # Process data
                data_processor = DataProcessor(df)
                filtered_data = data_processor.filter_data(category)
                if filtered_data.shape[0] == 0:
                    self.status_label.config(text=f"No data found for category: {category}")
                    return

                grouped_data = data_processor.group_data(filtered_data)
                final_data = data_processor.create_invoice_info(grouped_data)

                total_sale = data_processor.calculate_total_sale(final_data)

                outputfile_name = Helpers.generate_file_name(input_dir, category, "", file_name)
                # Generate PDF
                pdf_generator = PDFGenerator(outputfile_name)
                
                # Start the progress bar
                self.progress_bar.start()

                pdf_generator.generate_pdf(final_data.to_dict(orient='records'), header_data, total_sale)
                self.progress_bar.stop()
                print(f"PDF saved successfully at {outputfile_name}")
                self.status_label.config(text="PDF generated successfully.", fg="green")
                self.file_label.config(text="No file selected")
                self.file_path = None
                self.progress_bar['value'] = 100  # Indicate completion
                self.show_success_dialog(outputfile_name)
                # messagebox.showinfo("Success", f"PDF report generated: {absolute_path}")
            else:
                messagebox.showerror("Error", "No data found in 'Item Details' sheet.")

        except Exception as e:
            self.status_label.config(text=f"Error generating PDF: {e}", fg="red")
            messagebox.showerror("Error", f"Error generating PDF: {e}")
            self.progress_bar.stop()  # Stop the progress bar if there's an error



    def show_success_dialog(self, file_path):
        dialog = tk.Toplevel(self.root)
        dialog.title("Success")
        dialog.geometry("300x200")

        label = tk.Label(dialog, text=f"PDF report generated: {file_path}")
        label.pack(pady=10)

        open_button = tk.Button(dialog, text="Open PDF", command=lambda: os.startfile(file_path))
        open_button.pack(pady=10)

        def on_close():
            dialog.destroy()
            self.progress_bar['value'] = 0

        dialog.protocol("WM_DELETE_WINDOW", on_close)

        ok_button = tk.Button(dialog, text="OK", command=on_close)
        ok_button.pack(pady=10)

