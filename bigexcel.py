import csv
import os
from datetime import datetime, timedelta
#get a date based on days elapsed from start of snow year
def newDate(days_elapsed):
    base_date = datetime.strptime('2021-10-01', '%Y-%m-%d')
    new_date = base_date + timedelta(days=days_elapsed)
    return new_date.strftime('%Y%m%d')

def fileList(num_files):
    #from oct 1
    days_elapsed = 0
    #list of file names
    csv_files = [] 
    for i in range(1, num_files +1):
        csv_files.append("gucmetM1.b1." + newDate(days_elapsed) + ".000000.csv")
        days_elapsed +=1
    return csv_files

def onebigCSV(snowYearCSV, csv_files):
    with open(snowYearCSV, 'w') as output_file:
            writer = csv.writer(output_file)
            
            for file_name in csv_files:
                
                if not os.path.isfile(file_name):
                    print(f"Input file not found: {file_name}")
                    continue
                
                with open(file_name, 'r') as input_file:
                    reader = csv.reader(input_file)
                    writer.writerows(reader)
            
                print(f"Processed file: {file_name}")
    
    print(f"Compilation successful. Output file: {output_filename}")

output_filename = "compiled.csv"
file_prefix = "file"  # Update the file prefix if needed
num_files = 365

list = fileList(365)
onebigCSV(output_filename, list)