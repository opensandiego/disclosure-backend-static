import pandas

FILE = "file:///home/bolun/Documents/cal-data.xlsx"

A_SHEET = pandas.read_excel(FILE, sheet_name="A-Contributions")
C_SHEET = pandas.read_excel(FILE, sheet_name="C-Contributions")
I_SHEET = pandas.read_excel(FILE, sheet_name="I-Contributions")
D_SHEET = pandas.read_excel(FILE, sheet_name="D-Expenditure")
G_SHEET = pandas.read_excel(FILE, sheet_name="G-Expenditure")
E_SHEET = pandas.read_excel(FILE, sheet_name="E-Expenditure")


def sum_of_sheet_columns(summed_column, *args):
    '''
    returns sum of columns of the specified name on specified sheets
    Takes *args of sheets and a string of the column name
    '''
    total = 0
    for sheet in args:
        total += sheet[summed_column].sum()
    return total


def sum_of_unique_sheet_columns(identifier_column, summed_column, *args):
    '''
    returns pandas series with the sum each identifier's column
    combined from every sheet. Takes *args of sheets and a string of
    the column name and the identifier column
    '''
    dict_totals = {}
    for sheet in args:
        for c, identifier in enumerate(sheet[identifier_column]):
            if dict_totals.get(identifier) is None:
                dict_totals.update({identifier: sheet[summed_column].iloc[c]})
            else:
                num = dict_totals.get(identifier)
                + sheet[summed_column].iloc[c]
                dict_totals.update({identifier: num})
    return pandas.Series(dict_totals)


total_contributions = sum_of_sheet_columns("Tran_Amt2", A_SHEET, C_SHEET, I_SHEET)
total_expenditures = sum_of_sheet_columns("Amount", D_SHEET, G_SHEET, E_SHEET)
expenditures_by_zip = sum_of_unique_sheet_columns("Tran_Zip4", "Tran_Amt2",
                                                  A_SHEET, C_SHEET, I_SHEET)
expenditures_by_occupation = sum_of_unique_sheet_columns("Tran_Occ", "Tran_Amt2",
                                                         A_SHEET, C_SHEET, I_SHEET)

expenditures_by_zip.to_json("expenditures_by_zip.json")
expenditures_by_occupation.to_json("expenditures_by_occupation.json")

series_total_contributions = pandas.Series(total_contributions,
                                           index=["total_contributions"])
series_total_contributions.to_json("total_contributions.json")

series_total_expenditures = pandas.Series(total_expenditures,
                                          index=["total_expenditures"])
series_total_expenditures.to_json("total_expenditures.json")
