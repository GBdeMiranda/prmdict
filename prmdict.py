'''
Module for loading a Deal.II parameter file from a raw file or string input.
'''

import json

class prm_dict(dict):
    '''
    Class to load the Deal.II parameter file (.prm) from a file path or string input.
    '''

    def __init__ (self, file=None, file_path=None):
        # Initialize the parameter file from a file or string input.
        # If both are provided, the file will be used.
        # If neither are provided, an empty parameter file will be created.
        if file is not None:
            self.parse(file)
        elif file_path is not None:
            with open(file_path, 'r') as file:
                self.parse(file)
        else:
            super().__init__()


    def parse(self, file):
        """
        Parse a prm file and creates a dict.
        """
        root_object = prm_dict()
        section_stack = [root_object]
        for line in file:
            line = line.strip()
            
            if not line or line.startswith("#"):
                continue
            
            if line.startswith("subsection"):
                new_section = prm_dict()
                section_name = line[11:]
                section_stack[-1][section_name] = new_section
                section_stack.append(new_section)

            elif line.startswith("set"):
                tokens = line[4:].split("=")
                key = tokens[0].strip()
                value = tokens[1].strip()
                section_stack[-1][key] = value


            elif line.startswith("end"):
                section_stack.pop()

        super().__init__(root_object)


    def dict2prm(self, indentation_level=0):
        output = []
        indentation = "  " * indentation_level

        for key, value in self.items():
            if isinstance(value, dict):
                output.append(f"{indentation}subsection {key}")
                output.extend(value.dict2prm(indentation_level + 1))
                output.append(f"{indentation}end")
            else:
                output.append(f"{indentation}set {key} = {value}")

        return output


    def save_prm(self, file_path):
        """
        Save the output as a prm file in the specified path.
        """
        output = self.dict2prm()
        with open(file_path, "w") as prm_file:
            for line in output:
                prm_file.write(line + "\n")


    def find_key_path(self, key):
        """
        Find the path of a given key.
        XXX It will be a problem if more than one subsection has the same key XXX
        """
        for k, v in self.items():
            if k == key:
                return k
            if isinstance(v, dict):
                item = v.find_key(key)
                if item is not None:
                    # concatenate the keys
                    return k + '/' + str(item)


    def set(self, path, value):
        """
        Set a value in the parameter file using a path.
        """
        keys = path.split('/')
        if len(keys) == 1:
            self[keys[0]] = value
        else:
            if keys[0] not in self:
                self[keys[0]] = prm_dict()
            self[keys[0]].set('/'.join(keys[1:]), value)
