import csv
with open('Airports2.csv', newline='') as csvfile:
     airports = csv.reader(csvfile, delimiter=' ', quotechar='|')
     for row in airports:
       print(', '.join(row))