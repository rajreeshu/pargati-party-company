import pandas as pd

class DataProcessor:
    def __init__(self, df):
        self.df = df

    def getHeaderData(self, category):
        header_data = {}

    # Iterate through the DataFrame rows, assuming keys are in column 0 and values are in column 1
        for index, row in self.df.head(6).iterrows():
            key = row[0]  # Column 0 as key
            value = row[1]  # Column 1 as value
            if pd.notna(key) and pd.notna(value):  # Check for non-empty key and value
                key = str(key).strip()  # Convert to string and strip any leading/trailing spaces
                # Check if the key starts with "party" (case-insensitive) and remove it
                if key.lower().startswith('party'):
                    key = key[5:].strip()
                header_data[key] = value
                if key == "Duration":
                    break
        header_data["Company"]=category.upper()
        return header_data



    # def filter_data(self, category):
    #     return self.df[self.df['Category'].str.contains(category, case=False, na=False)]

    def filter_data(self, category):
        # Split the 'Category' column by '<>'
        split_categories = self.df['Category'].str.split('<>', expand=True)
        category_lower = category.lower()
        # Convert all entries to strings and then to lower case
        split_categories = split_categories.applymap(lambda x: str(x).lower() if pd.notnull(x) else x)

        # Initialize the mask
        mask = pd.Series([False] * len(split_categories), index=split_categories.index)

        # Iterate through each column to apply the contains check and debug each step
        for column in split_categories:
            for index, value in split_categories[column].items():
                if pd.notnull(value):  # Check for non-null values
                    contains_check = category_lower in value
                    if contains_check:
                        mask[index] = True
                        print(
                            f"Column: {column}, Index: {index}, Value: {value}, Contains '{category_lower}': {contains_check}")

        # Filter the dataframe based on the mask
        return self.df[mask]

    def group_data(self, df_filtered):
        return df_filtered.groupby('Item Name').agg({
            'Quantity': 'sum',
            'Amount': 'sum',
            'Invoice No./Txn No.': lambda x: ', '.join(x.astype(str)),
            'Date': lambda x: ', '.join(x.astype(str))
        }).reset_index()

    def create_invoice_info(self, df_grouped):
        df_grouped['Invoice_Info'] = df_grouped.apply(
            lambda row: ', '.join([
                f"{str(int(float(inv))) if inv.replace('.', '', 1).isdigit() else inv} ({date})"
                for inv, date in zip(
                    row['Invoice No./Txn No.'].split(', '), row['Date'].split(', ')
                )
            ]),
            axis=1
        )
        df_grouped['Invoice_Info'] = df_grouped['Invoice_Info'].astype(str)
        return df_grouped

    def calculate_total_sale(self, df_grouped):
        return df_grouped['Amount'].sum()
