import xml.etree.ElementTree as ET

def parse_and_remove(filename, path):
    path_parts = path.split('/')
    doc = ET.iterparse(filename, ('start', 'end'))
    # Skip the root element
    next(doc)
    tag_stack = []
    elem_stack = []
    for event, elem in doc:
        if event == 'start':
            tag_stack.append(elem.tag)
            elem_stack.append(elem)
        elif event == 'end':
            if tag_stack == path_parts:
                yield elem
            try:
                tag_stack.pop()
                elem_stack.pop()
            except IndexError:
                pass

type_of_government = set()  # set of government types

countries = parse_and_remove('mondial-3.0.xml', 'country')  # generator: produces country objects from XML

for country in countries:
    type_of_government.add(country.get('government').strip())

print(type_of_government, f'\nNumber of government types: {len(type_of_government)}')
