import camelot
import fitz
import re
import pandas as pd
from datetime import datetime


class AnnualReport:

    # regex pattern to identify digits with commas
    nPattern = r"[0-9]{1,3}(?:,[0-9]{3})+"

    # initialize class
    def __init__(self, file: str, bank: bool = False):
        self.file = file
        self.bank = bank

        # switch case to use different keyword feature attribute if company is a bank
        match bank:
            case True:
                self.features = {
                    "SOPL": ["interest income", "commission", "profit", "tax"],
                    "SOFP": ["financial position", "assets", "liabilities", "equity"],
                    "SOCF": ["cash flows", "operating activities", "investing activities", "financing activities"]
                }
            
            case False:
                self.features = {
                    "SOPL": ["profit or loss", "revenue", "expense", "profit", "tax"],
                    "SOFP": ["financial position", "assets", "liabilities", "equity"],
                    "SOCF": ["cash flows", "investing", "operating", "financing"]
                }

    # read pages of annual report pdf file
    def _read_report(self, file: str):
        pages = fitz.open(file)
        return pages
    
    # function to shift the column number by index number to help rearrange columns
    def _next_no(self, column_name: int, index: int) -> int:
        no = column_name + index
        return no

    def _split_columns(self, df: pd.DataFrame):

        casted = []
        for column in df.columns:
            # check for columns with newline character and append to casted list
            if any("\n" in str(val) for val in df[column]):
                if column == 0:
                    pass
                else:
                    casted.append(column)

        # iterate over casted columns with newline characters
        for i, number in enumerate(casted):
            # rename columns to accomodate new split column
            df.rename(columns={self._next_no(number, 1): self._next_no(number, 2)}, inplace=True)

            # split column by newline delimiter or "   "
            df[[number, self._next_no(number, 1)]] = df[number].str.split(pat="    |\n", n=1, expand=True, regex=True)
            if i < len(casted)-1:
                casted[i+1] += 1

        # rearrange column order
        df = df[[i for i in range(len(df.columns))]]

            
        return df
    
    
    def _clean_report(self):

        # organize financial table and remove unnecessary columns
        mask = self.table.iloc[:, 1:].apply(
            lambda col: col.isna().sum() > 20 or
            any(str(cell).lower().count("note") > 0 and len(str(cell)) < 10 for cell in col)
        )
        self.table = self.table.drop(columns=self.table.columns[1:][mask])
        self.table.columns = list(range(len(self.table.columns)))

        # Find rows with any empty cell and create a boolean mask
        empty_cells_mask = self.table.apply(lambda row: sum(row.apply(lambda cell: len(str(cell)) == 0)) > 1, axis=1)

        # Get the indices of rows with any empty cell
        indices_with_empty_cells = empty_cells_mask[empty_cells_mask].index

        # Get the first 3 and last 3 indices of the DataFrame
        hf = list(self.table.iloc[:3].index) + list(self.table.iloc[-3:].index)

        # Filter indices to get only those that are both in indices_with_empty_cells and hf
        indices_to_drop = [index for index in indices_with_empty_cells if index in hf]

        # Drop the unwanted rows from the DataFrame
        self.table.drop(index=indices_to_drop, inplace=True)
        
        # drop rows with up to three nan cell
        self.table.dropna(thresh=3, inplace=True)

        # drop columns with up to 15 nan cells
        self.table.dropna(thresh=15, axis="columns", inplace=True)

        # set dataframe index to line item description
        self.table.set_index(self.table.columns[0], inplace=True)

        
        return self.table


    # view tables on pages with financial report
    def _view_report(self, page_no: str):
        tables = camelot.read_pdf(
            self.file,
            flavor="stream",
            pages=page_no,
            edge_tol = 150
        )
        if len(page_no.split(",")) > 1:
            tablist = [self._split_columns(table.df) for table in tables]
            return tablist
        else:
            self.table = self._split_columns(tables[0].df)
            return self._clean_report()

    def report(self, type: str) -> pd.DataFrame:
        """
        This function reads the annual report and outputs the requested financial statement

        type: str variable
        'SOFP', statement of financial position
        'SOPL', statement of profit or loss
        'SOCF', statement of cash flow
        """
        
        self.type = type
        self.page_match = {}
        self.page_no = None  # Initialize self.page_no to None before the loop

        for index, page in enumerate(self._read_report(self.file)):
            self.page = page.get_text().lower()
            self.found = 0

            for feature in self.features[self.type]:
                if feature in self.page and re.search(AnnualReport.nPattern, self.page):
                    self.found += 1

            self.page_match[index] = self.found

        # list of number if keyword matches for each page
        values = list(self.page_match.values())

        # page number with highest matches
        self.match_page = values.index(max(values)) + 1

        # if all keyword matches are found
        if max(values) == len(self.features[self.type]):
            self.page_no = self.match_page
            return self._view_report(str(self.page_no))

        # if some keywords are found use the page with the highest number of matches
        elif max(values) < len(self.features[self.type]):
            self.page_no = []
            self.page_no.append(self.match_page)
            self.page_no.append(self.match_page + 1)
            self.page_no = [str(no) for no in self.page_no]
            self.page_no = ",".join(self.page_no)

            table = self._view_report(self.page_no)
            if table[0].shape[0] > 20:
                self.table = pd.concat(table)
                return self._clean_report()
        
        else:
            return None

    
    def save_report(self, type: str) -> None:

        """ Save financial report as csv file.
        type: SOFP - Statement of Financial Position
        SOCF - Statement of cash flow
        SOPL - Statement of profit or loss"""

        report = self.report(type)
        report.to_csv(f"{self.file[:-4]}-{type}.csv", encoding="utf-8-sig", header=False)