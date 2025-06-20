import glob
import os
import chardet
import json
import sys
import re

if len(sys.argv) != 2:
    print('Usage: python IAL_dependency_graph.py <search_directory>')
    sys.exit(1)

search_directory = sys.argv[1]
if not os.path.isdir(search_directory):
    print(f'Error: {search_directory} is not a valid directory')
    sys.exit(1)

print(f'Searching for Fortran files in {search_directory}...')

files = glob.glob(os.path.join(search_directory, '**', '*.F*'), recursive=True)
#files = ["/home/oli/dev/IAL/mpa/micro/externals/aro_lima.F90"]
#files = ["/home/oli/dev/IAL/arpifs/phys_dmn/apl_arome.F90"]

files = [f for f in files if os.path.isfile(f)]
print(f'Found {len(files)} files in {search_directory}')


lines_all = []
for file_number,file_path in enumerate(files, 1):

    if file_number % 1 == 0:
        print(f'Processing file {file_number} of {len(files)}: {file_path}')
    
    with open(file_path, 'rb') as f:
        raw_data = f.read()
        result   = chardet.detect(raw_data)
        encoding = result['encoding']

    file  = open(file_path, 'r', encoding=encoding, errors='ignore')
    lines = file.readlines()
    lines_all.append(lines)

print(f'Found {len(lines_all)} lines in {len(files)} files')

print('Finding types and type connections...')
types = []
type_connections = {}
types_used     = []
type_name = ""
intype = False

for fileid, lines in enumerate(lines_all,1):

    if fileid % 100 == 0:
        print(f'Processing file {fileid} of {len(lines_all)}')

    for line in lines:

        str = line.lstrip().rstrip()
        str = re.split(r"(?i)\s|,|IS|PUBLIC|::|\bextends\(\s*[^)]+\s*\)", str)

        str = list(filter(None, str))
        if str:
            if (str[0].lower()      == 'type' and 
                str[1].lower()[0:1] != '(' and 
                not intype):
                
                intype    = True
                type_name = str[1].replace('\n', '')
                types.append(type_name)
                
            elif (len(str)>1 and
                  str[0].lower() == 'end'  and 
                  str[1].lower() == 'type' and
                  intype ==True):# and str[2].lower().replace('\n', '') == type_name:
            
                intype = False

                if len(types_used)>0:
                    type_connections[type_name] = list(set( types_used))
                types_used = []

            elif (intype):
                str_list = list(filter(None,re.split(r"[()]", str[0])))
                if str_list[0].lower() == 'type':
                    if len(str_list)>1:
                        type_used = str_list[1]
                        if type_used not in types_used:
                            types_used.append(type_used)

print(f'Found {len(types)} types')

print('Saving types ...')
file_path = 'types.json'
with open(file_path, 'w') as json_file:
    json.dump(types, json_file, indent=4)

print('Saving type connections ...')
file_path = 'type_connections.json'
with open(file_path, 'w') as json_file:
    json.dump(type_connections, json_file, indent=4)