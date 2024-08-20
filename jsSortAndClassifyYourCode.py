import re
from pathlib import Path, PurePath
import numpy as np
import os
from jsCodeStructureDetection import GetElements, DisplayElements

def ReorderListByReference(lst, names_at_top=['constructor'], idx=0):
    """
    Reorders a list of elements, placing specified elements at the top.

    Args:
        lst (list of list): The list of elements to be reordered.
        names_at_top (list of str): A list of names that should be placed at the top.
        idx (int, optional): The index within each element to check against `names_at_top`. Defaults to 0.

    Returns:
        list: The reordered list with specified elements at the top.
    """
    elements_at_top = []
    remove_idx = []

    for i, l in enumerate(lst):         # For each element
        if l[idx] in names_at_top:      # If want to reorder it
            elements_at_top.append(l)   # Add it in the firsts one
            remove_idx.append(i)        # Remove it from the normal one


    if len(elements_at_top)>0:                                          # If reoder detected
        lst = [l for i, l in enumerate(lst) if i not in remove_idx]     # Get the list without that elements
        lst = elements_at_top + lst                                     # Concatenate the reoder to the clear list

    return lst

def ReconstructCodeRec(elements, lines, s, e, level=0):
    """
    Recursively reconstructs the code by reordering blocks and generating a header comment.

    Args:
        elements (list): The list of elements identified in the code.
        lines (list of str): The lines of the original code.
        s (int): The start index for processing.
        e (int): The end index for processing.
        level (int, optional): The current depth level of recursion. Defaults to 0.

    Returns:
        tuple: A tuple containing:
            - new_lines (list of str): The reconstructed lines of code.
            - header_comment (str): The header comment generated during reconstruction.
    """
    packs = []                          # code packs                      
    del_index = []                      # elements position to delete
    idx_s = idx_e = -1                  # Init the different positions
    new_lines = []                      # The new lines list
    header_comment = ''                 # The header comment
    code_at_the_end = []                # Code to add at the end

    for i, element in enumerate(elements):
        # If the element is between the bounds and (no prev end or the start is superior to it or (equal to it but the element is on mode than a single line) 
        if s<= element[1] and e>= element[2] and (idx_e==-1 or (element[1]>idx_e or (element[1]==idx_e and element[2]>element[1]))):

            # If the element is equal to the prev end (the line alredy add to new_line)
            if element[1]==idx_e:
                element[1] = idx_e+1    # Remove the display of the first line (can lead to trouble if code badly indent. Okay if code as if else)
            
            # The goal there is to group different blocks. If a function have a header comment, we want it to move with the function
            if idx_s == -1:         # If no element start
                idx_s = element[1]  # define the start 
                idx_e = -1          # ReInit the end

            del_index.append(i)     # The element is process so we can remove it

            # If the element is a block and we want to sort it (change is position)
            if element[0] in blocks_key and blocks[element[0]]['sort'] is True:
                packs.append([element[3], idx_s, element[1], element[2], element[0]])   # Add it to the pack
                idx_s = -1                                                              # ReInit the start
                idx_e = element[2]                                                      # Define the block end
            # If (the element is a block and we want to keep its position) or (the element is a single element and we want to keep its position)
            elif (element[0] in blocks_key and blocks[element[0]]['keep_position'] is True) or (element[0] in singles_key and singles[element[0]]['keep_position'] is True):
                code_at_the_end.extend(lines[idx_s:element[2]+1])   # Add it to the end of the code 
                idx_s = -1                                          # ReInit the start
                idx_e = element[2]                                  # Define the block end

    # If it have a start without end, add it to the end of code
    if idx_s!=-1:
        code_at_the_end.extend(lines[idx_s:e+1])

    elements = [item for index, item in enumerate(elements) if index not in del_index]  # Remove the undesired elements
    packs = sorted(packs, key=lambda x: x[0])                                           # Sort the desire blocks base on their name
    packs = ReorderListByReference(packs, names_at_top, idx=0)                          # Reorder them (exemple: constructor need to be at the top)

    for pack in packs:                                                                                  # For each packs
        n_l = lines[pack[1]:pack[3]]                                                                    # Get the lines of it
        rcr, head_com = ReconstructCodeRec(elements, lines, s=pack[1]+1, e=pack[3]-1, level=level+1)    # Get the reconstruc lines inside this pack

        # If no internal restructuration, add the pack lines
        if len(rcr)== 0:
            new_lines.extend(lines[pack[1]:pack[3]+1])
        # If an internal  restructuration, add the restructuration in the pack block
        else:
            new_lines.extend(lines[pack[1]:pack[2]+1])
            new_lines.extend(rcr)
            new_lines.append(lines[pack[3]])
        
        new_lines.append('')

        # Update the header comment
        header_comment += (comment_indent * level) + '- [' + pack[4] +'] ' + pack[0] +'\n'
        header_comment += head_com

    # If it have code at the end, add it
    if len(code_at_the_end)>0:
        new_lines.extend(code_at_the_end)
        new_lines.append('')


    return new_lines, header_comment

def GetLineType(elements, lines, type_='import'):
    """
    Extracts and returns code lines of a specified type, removing them from the original list.

    Args:
        elements (list): The list of elements identified in the code.
        lines (list of str): The lines of the original code.
        type_ (str, optional): The type of code lines to extract. Defaults to 'import'.

    Returns:
        tuple: A tuple containing:
            - new_code (list of str): The extracted lines of the specified type.
            - elements (list): The remaining elements after extraction.
            - lines (list of str): The remaining lines after extraction.
    """
    new_code = []
    del_index = []
    del_lines = set()

    for i, element in enumerate(elements):                                                  # For each elements
        if element[0] == type_:                                                             # If its the desire type
            del_index.append(i)                                                             # Add it to the delete one
            del_lines = del_lines.union(set(np.arange(element[1], element[2]+1)))           # Delete this lines too
            new_code.extend(lines[element[1]:element[2]+1])                                 # Add it to the new_code
    
    elements = [item for index, item in enumerate(elements) if index not in del_index]      # Delete the unwant elements
    lines = [item if index not in del_lines else '' for index, item in enumerate(lines) ]   # Delete the lines ('' because need to keep the lines length)

    # If new code, add an empty line
    if len(new_code)>0:
        new_code.append('')

    return new_code, elements, lines


def ReconstructCode(elements, lines):
    """
    Reconstructs the JavaScript code by reordering blocks, adding header comments, 
    and positioning certain single-line elements.

    Args:
        elements (list): The list of elements identified in the code.
        lines (list of str): The lines of the original code.

    Returns:
        list of str: The fully reconstructed code lines.
    """
    new_code = []

    # For the single items, get the one that need a special position (ex: import at the top)
    singles_codes = {}
    for type_, values in singles.items():
        if values['in_code_position'] is not None:
            singles_codes[type_], elements, lines = GetLineType(elements, lines, type_=type_)

    # Get the elements
    sorted_lines, header_comment = ReconstructCodeRec(elements, lines, s=0, e=len(lines))

    # Construct the header comment
    header_comment = '/*'+id+'\n'+header_comment+'*/\n'

    # Add the singles at the top of the code
    for type_, code in singles_codes.items():
        if singles[type_]['in_code_position'] == 'up':
            new_code.extend(code)

    new_code.append(header_comment) # Add the header comment
    new_code.extend(sorted_lines)   # Add the main code

    # Add the singles at the bottom of the code
    for type_, code in singles_codes.items():
        if singles[type_]['in_code_position'] == 'down':
            new_code.extend(code)

    return new_code

def MaxEmptyLine(lines, max_el=1):
    """
    Limits the number of consecutive empty lines in the code.

    Args:
        lines (list of str): The lines of the original code.
        max_el (int, optional): The maximum allowed number of consecutive empty lines. Defaults to 1.

    Returns:
        list of str: The lines with empty lines reduced according to `max_el`.
    """
    new_lines = []
    el = 0

    for line in lines:          # For each lines
        if line.strip() == '':  # If empty
            el+=1               # Add an occurence
        elif el>0:              # If not empty
            el=0                # Put the number of consecutive empty_lines to 0

        if el<= max_el:             # If the number of empty lines is okay
            new_lines.append(line)  # Add the line
    return new_lines

def RemoveLastsEmptyLines(lines):
    """
    Removes trailing empty lines from the code.

    Args:
        lines (list of str): The lines of the original code.

    Returns:
        list of str: The lines without trailing empty lines.
    """
    for i in range(len(lines)-1, -1, -1):   # For all lines starting from the end
        if lines[i].strip() == '':          # If it's an empty line
            lines.pop(i)                    # Remove it
        else:                               # If it's not an empty line 
            return lines                    # Return them
    return lines

def PofiningCode(code):
    """
    Applies final formatting to the code by limiting empty lines and removing trailing empty lines.

    Args:
        code (list of str): The lines of the code.

    Returns:
        list of str: The formatted lines of code.
    """
    new_code = code
    new_code = MaxEmptyLine(lines=new_code, max_el=1)
    new_code = RemoveLastsEmptyLines(lines=new_code)

    return new_code

def process_file(file_path_inp, file_path_out):
    """
    Processes a JavaScript file, reordering its elements and formatting the output.

    Args:
        file_path_inp (str or Path): The path to the input JavaScript file.
        file_path_out (str or Path): The path to save the processed JavaScript file.

    Returns:
        None: This function writes the output directly to the specified file.
    """
    # Read the input file
    with open(file_path_inp, 'r') as file:
        code = file.read()

    # Get the lines
    lines = code.split('\n')        
    # Get the elements                                
    elements = GetElements(lines, blocks, singles, ignore = [id])

    # Get the new code
    new_code = ReconstructCode(elements, lines)
    new_code = PofiningCode(new_code)

    # Write the sorted code back to the file
    with open(file_path_out, 'w') as file:
        file.write('\n'.join(new_code))

if __name__ == "__main__":
    singles = {
        'comment':{
            'element':'//',
            'way':'startswith',
            'position':'up',
            'in_code_position':None,
            'keep_position':False
        },
        'empty':{
            'element':'',
            'way':'==',
            'position':'up',
            'in_code_position':None,
            'keep_position':False
        },
        'import':{
            'element':'import',
            'way':'startswith',
            'position':'up',
            'in_code_position':'up',
            'keep_position':False
        },
        'export':{
            'element':'export',
            'way':'startswith',
            'position':'down',
            'in_code_position':'down',
            'keep_position':False
        },
        'other':{
            'element':'',
            'way':'no (,),{,},/*,*/',
            'position':'down',
            'in_code_position':None,
            'keep_position':True
        },
        'default':{
            'element':'',
            'way':'',
            'position':'default',
            'in_code_position':None,
            'keep_position':False
        },
    }
    singles_key = list(singles.keys())    # The blocks types

    # Block parameters
    blocks = {
        'comment_block':{
            'pattern': r'\/\*',
            'have_args':False,
            'is_inside':[],
            'is_not_in':['comment_block'],
            'recursive':False,
            'sort':False,
            'open':'/*',
            'close':'*/',
            'keep_position':False
        },
        'class':{
            'pattern': r'\bclass(?:\s+(\w*))?\b',   # Pattern for identify the start of the block
            'have_args':False,                      # If args, open and close start once parenthesis close # todo improve it (veryfy if something open before the open char. If the case wait it to close)
            'is_inside':[],                         # It is present in others defined blocks ? (Empty = all allow)
            'is_not_in':['comment_block'],          # It can't be present in some defined blocks ? (Empty = all allow)
            'recursive':True,                       # Do we want it's content be process ?
            'sort':True,                            # Do we want to sort this blocks ?
            'open':'{',                             # str that open the block
            'close':'}',
            'keep_position':False                   # str that close the block
        },
        'function':{
            'pattern': r'\bfunction\s+(\w+)\s*\(', 
            'have_args':True,
            'is_inside':[],
            'is_not_in':['comment_block'],
            'recursive':True,
            'sort':True,
            'open':'{',
            'close':'}',
            'keep_position':False
        },
        'function_arrow':{
            'pattern': r'\bconst\s+\(\s*(\w+)\s*=\s*\([^)]*\)\s*=>\s*',
            'have_args':False,
            'is_inside':[],
            'is_not_in':['comment_block'],
            'recursive':True,
            'sort':True,
            'open':'(',
            'close':')',
            'keep_position':False
        },
        'function_arrow_':{
            'pattern': r'\bconst\s+(\w+)\s*=\s*\([^)]*\)\s*=>\s*',
            'have_args':False,
            'is_inside':[],
            'is_not_in':['comment_block'],
            'recursive':True,
            'sort':True,
            'open':'{',
            'close':'}',
            'keep_position':False
        },
        'methods':{
            'pattern': r'\b(\w+)\s*\([^)]*\)\s*',
            'have_args':True,
            'is_inside':['class'],
            'is_not_in':['methods', 'function', 'function_arrow', 'comment_block', 'function_call', 'other_multi'],
            'recursive':False,
            'sort':True,
            'open':'{',
            'close':'}',
            'keep_position':False
        },
        'other_multi':{
            'pattern': r'\b.*\{',
            'have_args':False,
            'is_inside':[],
            'is_not_in':['comment_block'],
            'recursive':False,
            'sort':False,
            'open':'{',
            'close':'}',
            'keep_position':True
        },
        'function_call':{
            'pattern': r'\b\w+\s*\(+',
            'have_args':False,
            'is_inside':[],
            'is_not_in':['comment_block'],
            'recursive':False,
            'sort':False,
            'open':'(',
            'close':')',
            'keep_position':True
        }, 
    }

    blocks_key = list(blocks.keys())    # The blocks types

    comment_indent = '   '              # Indent to apply at the header comment
    id = "ELEMENTS NAME SUMMARY"        # Id for identify the header comment from the others code elements
    names_at_top = ['constructor']      # blocks name to add at the top

    # Path to the JavaScript file
    folder = Path('C:\\Users\\T0300487\\Downloads')
    extention = '.js'

    files_name = []#['name']            # The files name to process
    folders_path = ['C:\\Users\\T0300487\\Downloads']   # The folder with the js to process
    suffix = '_new' # Suffix to add at the new file for not overwrite the current one in case it have a problem

    # Process the folders
    for folder_path in folders_path:
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                file_p = Path(file)
                if file.endswith(extention) and not str(file_p.stem).endswith(suffix):
                    path_in = PurePath(root, file)
                    path_ou = PurePath(root, file_p.stem + suffix+extention)
                    process_file(file_path_inp=path_in, file_path_out=path_ou)

    # Process the files
    for file_name in files_name:
        path_in = PurePath(folder, file_name+extention)
        path_ou = PurePath(folder, file_name+suffix+extention)
        process_file(file_path_inp=path_in, file_path_out=path_ou)
