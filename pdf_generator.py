from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import Spacer
from reportlab.lib import fonts

from helpers import Helpers



class PDFGenerator:

    def __init__(self, output_path):
        self.output_path = output_path

    def generate_pdf(self, data, header_data, total_sum):
        styles = getSampleStyleSheet()
        pdf = SimpleDocTemplate(str(self.output_path), pagesize=letter,
                                rightMargin=30, leftMargin=30, topMargin=30, bottomMargin=18)
        elements = []
        # Add header section to elements, extend with header items
        header_elements = self.create_header(header_data)
        elements.extend(header_elements)  # Use extend instead of append

        elements.append(Spacer(1, 0.2 * inch))

        # Add table section for data
        elements.append(self.create_table(data, total_sum))

        # total_paragraph = Paragraph(f"<b>Total:</b> {total_sum:.2f}", styles['Normal'])
        # elements.append(total_paragraph)  # Append the paragraph directly

        pdf.build(elements)
    
    def create_header(self, header_data):
        """
        Creates a header section from the dictionary `header_data`.
        """
        styles = getSampleStyleSheet()
        header_elements = []

        # Add each key-value pair in the dictionary as a Paragraph
        for key, value in header_data.items():
            header_elements.append(Paragraph(f"<b>{key.capitalize()}:</b> {value}", styles['Normal']))

        return header_elements

    def create_table(self, data, total_sum):
        styles = getSampleStyleSheet()
        table_data = [['Item Name', 'Quantity', 'Pre-Tax', 'Post-Tax', 'Total Amount', 'Invoice Info']]  # Header
        total_sum =0
        total_quantity =0
        data=sorted(data, key=lambda x: x['Quantity'], reverse=True)
        for row in data:

            average_price = row['Amount'] / row['Quantity']  # post-tax amount
            pre_tax_amount = average_price / 1.18  # Calculate Pre-Tax Amount
            table_data.append([
                Paragraph(row['Item Name'], styles['BodyText']),
                Paragraph(str(row['Quantity']), styles['BodyText']),
                Paragraph(Helpers.format_amount(pre_tax_amount), styles['BodyText']),  # Pre-Tax Amount
                Paragraph(Helpers.format_amount(average_price), styles['BodyText']),  # post-Tax Amount
                Paragraph(Helpers.format_amount(row['Amount']), styles['BodyText']),
                Paragraph(str(row['Invoice_Info']), styles['BodyText'])
            ])
            total_sum += row['Amount']
            total_quantity += row['Quantity']

        table_data.append(["Total",Helpers.format_amount(total_quantity),"","",Helpers.format_amount(total_sum),""])


        table = Table(table_data)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.red),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))

        # Adjust column widths
        table._argW[0] = 2.8 * inch  # Item Name width
        table._argW[1] = 0.7 * inch  # Quantity width
        table._argW[2] = 0.8 * inch  # Average Price width
        table._argW[3] = 0.8 * inch  # Pre-Tax Amount width
        table._argW[4] = 1 * inch  # Total Amount width (reduced)
        table._argW[5] = 1.5 * inch  # Invoice Info width (increased)
        
        return table
    
        
