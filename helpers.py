from babel.numbers import format_currency,format_decimal
import os
from pathlib import Path

class Helpers:

    @staticmethod
    def format_amount(amount):
        """Formats the amount into Indian numbering system with ₹ symbol."""
        return format_decimal(amount, locale='en_IN')

    @staticmethod
    def generate_file_name(directory, company_name, party_name, base_filename):
        # Append company name and party name to the file name
        output_filename = f"{company_name}_{party_name}_{base_filename}.pdf"
        output_path = Path(directory) / output_filename

        # Check if the file already exists and append a number if necessary
        counter = 2
        while output_path.exists():
            output_filename = f"{company_name}_{party_name}_{counter}_{base_filename}.pdf"
            output_path = Path(directory) / output_filename
            counter += 1

        return output_path
