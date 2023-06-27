import csv

def create_dot_file(csv_file, dot_file):
    with open(csv_file, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header row

        with open(dot_file, 'w') as output:
            output.write('graph FamilyTree {\n')
            for row in reader:
                pid = row[0]
                name = row[1]
                parentId1 = row[12]
                parentId2 = row[13]
                
                if parentId1:
                    output.write(f'  "{parentId1}" -- "{pid}" [label="Child 1 of"];\n')
                if parentId2:
                    output.write(f'  "{parentId2}" -- "{pid}" [label="Child 2 of"];\n')
                
                output.write(f'  "{pid}" [label="{name}"];\n')
            
            output.write('}')
    
    print(f'DOT file "{dot_file}" created successfully.')

# Example usage:
create_dot_file('family.csv', 'family.dot')
