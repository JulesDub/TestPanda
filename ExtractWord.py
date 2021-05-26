import pandas as pd
from docx import Document


# Solution retenue : https://stackoverflow.com/questions/46618718/python-docx-to-extract-table-from-word-docx
# A regarder aussi possiblement : https://stackoverflow.com/questions/47977367/how-to-create-a-dataframe-from-a-table-in-a-word-document-docx-file-using-pan/47978006#47978006
document = Document("WORD_file/Fiche dispositif_RINBIO.docx")
table = document.tables[0]

data = []

keys = None

for i, row in enumerate(table.rows):
    text = (cell.text for cell in row.cells)

    if i == 0:
        keys = tuple(text)
        continue
    row_data = dict(zip(keys, text))
    data.append(row_data)
    #print (data)

df = pd.DataFrame(data)

#df["name"].tolist()
#print(df) # [5,6,7,8] - column with name 1

print("Glenn")
#Récupération des Sous-Programmes :
sous_programme=df.iloc[0,1]

#Récupération des Critères BEE
#print(df.iloc[8,:].tolist())

#Récupération des OE
#print(df.iloc[9,:].tolist())

#Récupération Paramètres
#print(df.iloc[11,:].tolist())

#Récupération information de bancarisation
#print(df.iloc[14,:].tolist())
print(df.iloc[14,1])