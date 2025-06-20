import glob
import os
import chardet
import json
import sys


file_path = 'subroutines.json'
with open(file_path, 'r') as file:
    subroutines = json.load(file)
subroutines = list(set(subroutines))
print(f'Loaded {len(subroutines)} nodes from {file_path}')

file_path = 'subroutines_called.json'
with open(file_path, 'r') as file:
    subroutines_called = json.load(file)
subroutines_called = list(set(subroutines_called))
print(f'Loaded {len(subroutines_called)} nodes from {file_path}')


subroutines = [s.replace('\n', '') for s in subroutines]
subroutines_called = [s.replace('\n', '') for s in subroutines_called]

print(f'Found {len(subroutines_called)} subroutines_called')
subroutines_called = set(subroutines_called).intersection(subroutines)
print(f'Found {len(subroutines_called)} subroutines_called')



subroutines_not_used = set(subroutines).difference(subroutines_called)

print(f'Found {len(subroutines_not_used)} subroutines not used:')
print(subroutines_not_used)