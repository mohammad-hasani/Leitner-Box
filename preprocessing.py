def load_file():
    with open('./words.txt', 'r') as f:
        data = f.readlines()
    return data


def concat_words(data):
    data2 = list()
    for i, v in enumerate(data):
        if len(v) > 20:
            data2.append(v)
        if len(v) < 20:
            if i > 0 and len(data2) > 0:
                data2[len(data2) - 1] += " " + v
    return data2


def split_words(data):
    dictionary = dict()
    for d in data:
        try:
            _ = d.split(':')
            dictionary[_[0]] = _[1]
        except:
            pass
    return dictionary


def clean_data(data):
    for key in data:
        data[key] = data[key].replace('\n', ' ')
    return data


def main():
    data = load_file()
    data = concat_words(data)
    data = split_words(data)
    data = clean_data(data)

    return data


import pandas as pd


def main2():
    xls = pd.ExcelFile(r"./data/Wortliste_MacmillanGatewayB2.xls")

    sheetX = xls.parse(0)

    columns = sheetX.columns
    print(sheetX)
    print(sheetX['Unnamed: 2'])
    # sheetX = sheetX.drop(sheetX[sheetX['Unnamed: 2'].isna()].index)
    # sheetX = sheetX.drop(sheetX[sheetX['Unnamed: 2'].isnull()].index)

    sheetX = sheetX[sheetX['Unnamed: 2'].isna() == False]

    print(sheetX)
    print(sheetX['Unnamed: 2'])

    # sheetX.to_excel('test.xls', sheet_name='test')
    return sheetX






####################################################################

#delete pronunciation
#recollect for b1 and b2, check the xlsx
# delete examples
# recollect from langescheit