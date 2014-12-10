import sys
import re
import csv

columnNamesSet = set()
itemsets = []

inputName = "data2.csv"
outputName = 'eggs.csv'

with open(inputName) as f:
  for line in f:
    m = re.search("{(?P<data>.*)}.*(?P<support>[0-9]\.[0-9]+)" ,line)
    if m is None:
      continue
    
    item = m.group('data')
    itemValues = {}
    for pair in item.split(","):
      key_val = pair.split("=")
      columnNamesSet.add(key_val[0])
      itemValues[key_val[0]] = key_val[1]

    itemsets.append((itemValues,m.group('support') ))

with open(outputName, 'wb') as csvfile:
  columnNames = list(columnNamesSet)
  spamwriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
  spamwriter.writerow(["Id"] + columnNames + ["Support", "#Items"])
  id = 1
  for items, sup in itemsets:
    line = [id]
    for column in columnNames:
      if column in items:
        line.append(items[column])
      else:
        line.append("")
    line.append(sup)
    line.append(len(items))
    spamwriter.writerow(line)
    id += 1

    
    
    
    
    