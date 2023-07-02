import csv
#check incrementing and compare to file
#function to average non-time values in a window (ex. window = 60 to get hourly avg from minutely data)
def entry_avg(window, input_csv, output_csv):
    data = []
    
    with open(input_csv, 'r') as csv_file:
        reader = csv.reader(csv_file)
        header = next(reader)  # Read the header with column titles
        
        #list to handle time (non averaged) data
        leftmost_column = []
        
        #list for other values with size of all cols -1
        column_sums = [0] * (len(header) - 1) 
        
        count = 0
        
        rows = list(reader)
        reverse = reversed(rows)
                
        for row in reverse:
            #if on a 60th row append time value to left col
            #potential bug
            if count % window == 0:
                leftmost_column.append(row[0])
                #print(row[0])

            for j in range(1, len(row)):  # Exclude leftmost column
                try:
                    column_sums[j-1] += float(row[j])
                except ValueError:
                    pass  # Ignore the entry if it cannot be cast to float

            count += 1
        
            if count % window == 0:
                averages = [leftmost_column[-1]]  # First value of leftmost column
                averages.extend([sum / window for sum in column_sums])
            
                data.append(averages)
                column_sums = [0] * (len(header) - 1)  # Reset column sums
        
    with open(output_csv, 'w') as csv_output:
        writer = csv.writer(csv_output)
        writer.writerow(header)  # Write the header
        writer.writerows(data)  # Write the averages

    print(f"Averages calculated and saved to {output_csv}")

# change for each use:
input_filename = "snowyear1Minute.csv"
output_filename = "snowyear1_Hourly.csv"
entry_avg(60, input_filename, output_filename)