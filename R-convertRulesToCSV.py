import sys
import re
import csv

columnNamesSet = set()
itemsets = []

inputName = "rules.csv"
outputName = 'eggs.csv'

with open(inputName) as f:
  with open(outputName, "w") as out:
    out.write("id,rule_l,rule_r,support,confidence,lift\n")
    itercars = iter(f)
    next(itercars)
    for line in itercars:
      out.write(line.replace(" => ", ","))
