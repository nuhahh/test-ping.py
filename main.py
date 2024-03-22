import os
import pandas as pd
import numpy as np
import xlsxwriter
import subprocess
import xlwt
import openpyxl
#################################################################################################################
#import xlsxwriter

# Create workbook objects for output files
workbook2 = xlsxwriter.Workbook('Dataset.xlsx')
workbook = xlsxwriter.Workbook('Average.xlsx')

# Add worksheets to the workbooks
worksheet = workbook.add_worksheet()
worksheet1 = workbook2.add_worksheet()

#########################################################################################################

# Specify the path to the dataset CSV file
dataset_path = "C:\\Users\\ALFA\\Downloads\\Desktop\\بحث\\Dataset-Unicauca-Version2-87Atts.csv"

# Specify the maximum number of IP addresses to extract
max_ips = 15

# Read the dataset CSV file
df = pd.read_csv(dataset_path)

# Extract the 'Destination.IP' column
destination_ips = df['Destination.IP']

# Remove duplicate IP addresses
unique_ips = destination_ips.drop_duplicates()

# Check if the number of unique IP addresses is less than or equal to max_ips
if len(unique_ips) <= max_ips:
     extracted_ips = unique_ips
else:
     extracted_ips = unique_ips[:max_ips]

# Print the  IP addresses
print("IP addresses:")
for ip in extracted_ips:
    print(ip)

# # Specify the output folder
output_folder = "C:\\Users\\ALFA\\Downloads\\Desktop\\New folder\\"
#
# # Save the extracted IP addresses to the file "aaa.txt"
output_file = os.path.join(output_folder, "aaa.txt")
np.savetxt(output_file, extracted_ips, fmt='%s')
################################################################################################################

# Read the IP addresses from the file "aaa.txt"
with open(output_file, 'r') as file:
    ip_addresses = file.read().splitlines()

# read Ip from file
f = open("C:\\Users\\ALFA\\Downloads\\Desktop\\New folder\\ip_average.txt", 'w')
with open("C:\\Users\\ALFA\\Downloads\\Desktop\\New folder\\aaa.txt") as file:
    Ip_ping = file.read()
    Ip_ping = Ip_ping.splitlines()
    row = len(Ip_ping)

    # repeat ping for each ip according enter count
    count = 1
    # work ping for each ip
    for ip in range(row):
        for j2 in range(count):
            print('Num_IP=', ip, '    Pinging now :   (', j2, ')    ', Ip_ping[ip])
            t = os.popen(f"C:\Windows\System32\ping  {Ip_ping[ip]}").read()
            print(t)
            data_ping = t.split("\n")[-2].split(",")

            # find average
            Average = data_ping[-1].split("=")[-1].strip(" ").strip("ms")
            print("Average =", Average)

            # write average for each ip to file(ip_average)
            f.write(Average + '\n')
f.close()
################################################################################################################
# read from file to find Result array
with open("C:\\Users\\ALFA\\Downloads\\Desktop\\New folder\\ip_average.txt") as file2:
    IP_Average = file2.read()
    IP_Average = IP_Average.splitlines()
row = len(Ip_ping)
col = row
c2 = count + 1
Result = [[0 for i in range(col)] for j in range(c2)]
sum1 = [0 for i in range(col)]
mean = [0 for i in range(col)]
after = [[0 for i in range(col)] for j in range(c2)]

# write the result array to excel
for i in range(row):
    worksheet.write(0, (i), Ip_ping[i])  # add header represent ip
    j1 = 0
    for j2 in range(col):
        for j in range(1, c2):


            # assignment to result array
            Result[0][i] = Ip_ping[i]
            Result[j][j2] = IP_Average[j1]
            worksheet.write(j, j2, Result[j][j2])  # write to excel the average
            j1 += 1
workbook.close()
################################################################################################################
# this step to find array content 0 or 1
import numpy as np

# Calculate sum and mean
for j in range(col):
    total_sum = 0  # Renamed variable from 'sum' to 'total_sum'
    count_vals = 0
    for i in range(1, c2):
        try:
            value = Result[i][j]
            if value != '':
                total_sum += float(value)
                count_vals += 1
        except ValueError as e:
            print(f"Invalid literal for float(): {value}")
    sum1[j] = total_sum
    mean[j] = total_sum / count_vals if count_vals > 0 else 0

print(sum1, "   ")
print(mean)

# Calculate standard deviation for each average value
std_deviation = np.std(mean)

# Calculate coefficient for each average value
coefficient = np.std(mean) / np.mean(mean)

# Define the 'after' array outside the loop
#after = [[0] * col for _ in range(c2)]

# Print standard deviation and coefficient for each average value
for j in range(col):
    print(f"Average {j+1}:")
    print("Standard Deviation:", std_deviation)
    print("Coefficient:", coefficient)
    print()

# Define the 'after' array outside the loop
after = [[0] * col for _ in range(c2)]

# Assign values to 'after' based on the threshold
threshold = coefficient
for i in range(1, c2):
    for j in range(row):
        value = Result[i][j]
        if value != '':
            if threshold > float(value):
                after[i][j] = 1
            if threshold < float(value):
                after[i][j] = 0
print("Threshold:", threshold)

for i in range(1, c2):
    for j in range(col):
        print(after[i][j], end="      ")
    print("\n")

    n = 0
for i in range(0, row):
    worksheet1.write(0, (i), Ip_ping[i])  # add header represent ip
for i in range(1, c2):
    for j in range(col):
        worksheet1.write(i, j, after[i][j])  # wite to excel the average

workbook2.close()
####################################################################################################################
