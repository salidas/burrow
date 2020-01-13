from pathlib import Path

class Ignorer:

    def get_entries(self, show_lookup_field=True):
        # if show_lookup_field:
        return self.entries
        # else:
        #     # Because self.entries is a list of dictionaries, we need to do a deep copy.
        #     # Otherwise, the dictionary objects in the new list still refere to the original list's
        #     # dictionary objects.
        #     import copy
        #     tmp_copy = copy.deepcopy(self.entries)
        #     for entry in tmp_copy:
        #         del entry["reported"]
        #     return tmp_copy


    def pretty_print_list(self):
        for entry in self.entries:
            text = entry["filename"]
            if entry["type"] == "line":
                text += ":" + entry["line"]
            print(text)


    def is_file_loaded(self):
        return self.file_loaded


    def is_file_ignored(self, filename):
        for entry in self.entries:
            if entry["type"] is "whole":
                if entry["filename"] == filename:
                    return True
        return False


    def is_line_ignored(self, filename, line):
        for entry in self.entries:
            if entry["type"] is "line":
                if entry["filename"] == filename:
                    if entry["line"] == str(line):
                        return True
        return False


    def load_ignore_file(self):
        # if verbose:
        #     print("[verbose] searching target directory for .burrowignore file...")
        if Path(self.burrowignore_filepath).is_file():
            if self.verbose:
                print("[verbose] found .burrowignore file!")
            with open(self.burrowignore_filepath, "r") as burrowignore_fileobject:
                for line in burrowignore_fileobject:
                    entry = line.split(":")
                    # print(entry, len(entry))
                    if len(entry) == 1:
                        self.entries.append(
                            {
                                "filename": entry[0],
                                "type": "whole",
                                "line": "N/A",
                                # "reported": False
                            }
                        )
                    else:
                        filename = entry[0]
                        line = entry[1].rstrip()
                        # print(filename, line)
                        self.entries.append(
                            {
                                "filename": filename,
                                "type": "line",
                                "line": line,
                                # "reported": False
                            }
                        )
            self.file_loaded = True
            return True
        return False


    def __init__(self, target_directory, verbose):
        self.entries = []
        self.burrowignore_filepath = target_directory + "/.burrowignore"
        self.file_loaded = False
        self.verbose = verbose
        self.load_ignore_file()