import os
import csv
from pathlib import Path

import tabula

def save_csv_file(new_file_name, data, headers):
    with open(new_file_name, 'w', encoding="utf-8",newline='') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=headers)
        writer.writeheader()
        writer.writerows(data)
        print(f"Se ha generado el archivo {new_file_name} de forma exitosa...")
        

def add_data_to_table(dataframe, csv_file):
    print(dataframe)
    print(csv_file)

def get_pdf_table(full_file_name):
   table = tabula.read_pdf(full_file_name,stream=True)
   df_table = table[0]
   df_table.rename(columns={"Unnamed: 0": "Disability Category", 
                            "Unnamed: 1": "Participants",
                            "Unnamed: 2": "Ballots Completed",
                            "Unnamed: 3": "Ballots Incomplete/Terminated",
                            "Unnamed: 4": "Accuracy",
                            "Results": "Time to Complete"}, inplace=True)
   # Remove data not relevant
   df_table_reduced = df_table.iloc[6:]
   #print(df_table_reduced)
   table_dict =  df_table_reduced.to_dict(orient='records')
   return table_dict
   
# def read_pdf_file(full_file_name):
#     reader = PdfReader(full_file_name)
#     page = reader.pages[0]
#     print(page.extract_text())

def main():
    data = [] # will store all rows from all files
    
    # Get the list of files in the folder "files"
    root_folder = os.getcwd()
    files_folder = Path(root_folder, "files")
    
    #files_list =  os.listdir("files")
    files_list = os.listdir(files_folder)
    
    counter = 1
    for file in files_list:
        print(f"File No. {counter}")
        full_file_name = Path(files_folder, file)
        print(full_file_name)
        #read_pdf_file(full_file_name)
        data_dict = get_pdf_table(full_file_name)
        print(data_dict)
        for item in data_dict:
            data.append(item)
        counter += 1
    
    headers = ["Disability Category", "Participants",
               "Ballots Completed", "Ballots Incomplete/Terminated",
               "Accuracy","Time to Complete"]
    print("--------------------")
    print(f"Se leyeron {len(files_list)} archivos.")
    print(f"En total se realizo la extraccion de {len(data)} filas")
    print(data)
    filename = "datos.csv"
    save_csv_file(filename, data, headers)
        
if __name__ == "__main__":
    main()