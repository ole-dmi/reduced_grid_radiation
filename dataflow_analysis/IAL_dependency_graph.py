import glob
import os
import chardet
import json
import sys

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

    if file_number % 100 == 0:
        print(f'Processing file {file_number} of {len(files)}: {file_path}')
    
    with open(file_path, 'rb') as f:
        raw_data = f.read()
        result   = chardet.detect(raw_data)
        encoding = result['encoding']

    file  = open(file_path, 'r', encoding=encoding, errors='ignore')
    lines = file.readlines()
    lines_all.append(lines)

print(f'Found {len(lines_all)} lines in {len(files)} files')

print('Finding subroutines...')
subroutines = []
subroutines_called = []
for fileid, lines in enumerate(lines_all,1):

    if fileid % 100 == 0:
        print(f'Processing file {fileid} of {len(lines_all)}')

    for line in lines:
 
        str = line.lstrip().split(" ")
        str = list(filter(None, str))
 
        if(str and str[0].lower()== 'subroutine'):
            subroutines.append(str[1].lower().split("(")[0])
        
        elif str and str[0].lower() == 'call':
            subroutine_call = str[1].split("(")[0].lower()
                
            if subroutine_call not in subroutines_called:
                subroutines_called.append(subroutine_call)

print(f'Found {len(subroutines)} subroutines')

print('Saving subroutines...')
file_path = 'subroutines.json'
with open(file_path, 'w') as json_file:
    json.dump(subroutines, json_file, indent=4)

print('Saving subroutines called...')
file_path = 'subroutines_called.json'
with open(file_path, 'w') as json_file:
    json.dump(subroutines_called, json_file, indent=4)


asdf
print('Finding subroutine connections...')
subroutine_connections = {}
subroutines_called     = []

insubroutine = False

for fileid, lines in enumerate(lines_all,1):

    if fileid % 100 == 0:
        print(f'Processing file {fileid} of {len(lines_all)}')

    for line in lines:

        str = line.lstrip().split(" ")
        str = list(filter(None, str))
                
        if str:
                
            if  str[0].lower() == 'subroutine' and not insubroutine:

                print(str)
                insubroutine = True
                subroutines_called.clear()
                subroutine_name = str[1].split("(")[0].lower()

            elif str[0].lower() == 'end' and str[1].lower() == 'subroutine' and str[2].lower().replace('\n', '') == subroutine_name:
            
                insubroutine = False
                if len(subroutines_called)>0:
                    subroutine_connections[subroutine_name] = list(set( subroutines_called))
            
            elif str[0].lower() == 'call':

                subroutine_call = str[1].split("(")[0].lower()
                
                if subroutine_call not in subroutines_called:
                    subroutines_called.append(subroutine_call)



file_path = 'subroutine_connections.json'
with open(file_path, 'w') as json_file:
    json.dump(subroutine_connections, json_file, indent=4)