from pathlib import Path

class Ignorer:


    def get(self, show_lookup_field=True):
        return self.entries


    def pretty_print_list(self):
        for entry in self.get():
            text = "- " + entry["match"]
            if entry["type"] == "line":
                text += ":" + entry["line"]
            print(text)


    def remove_ignored_entries(self, target_files):
        """
        Looks for and removes entries to be scanned if they are either:
        1) a .burrowignore file
        2) children of an ignored directory
        3) an ignored file

        entries involving line reductions 
        """

        tmp_target_list = []

        # For each submission...
        for target_entry in target_files:

            allow = True

            # Is this the .burrowignore file itself?
            # If so, skip and go to the next file.
            if target_entry.endswith(".burrowignore"):
                continue

            # Go through each burrowignore entry
            for ignore_entry in self.get():

                ignore_match = ignore_entry["match"]
                ignore_type = ignore_entry["type"]

                # Is this entry for a directory?
                if ignore_type == "directory":

                    # Does the entry start with the ignore entry?
                    if target_entry.startswith(ignore_match):
                        allow = False

                # Is this entry for a filename?
                elif ignore_type == "file":

                    # Does the entry exactly match the ignored filename?
                    if target_entry == ignore_match:
                        allow = False

            if allow:
                # The file has passed our sieve; add it to the list
                tmp_target_list.append(target_entry)

        return tmp_target_list


    def is_file_loaded(self):
        return self.file_loaded


    def is_line_ignored(self, name, line):
        for entry in self.get():
            if entry["type"] is "line":
                if entry["match"] == name:
                    if entry["line"] == str(line):
                        return True
        return False

    
    def load_ignore_file(self, parent_dir): 

        import os

        if self.verbose:
            print("[verbose] searching target directory for .burrowignore file...")

        # Check if the .burrowignore file exists
        if os.path.isfile(self.path):

            if self.verbose:
                print("[verbose] found .burrowignore file!")

            with open(self.path) as ignore_file:
                
                for entry in ignore_file:

                    # We call rstrip as well because line also includes includes the break from the file
                    entry_path_relative = os.path.join(parent_dir, entry.rstrip())     

                    lp_split = entry_path_relative.split(":")

                    # If the length is greater than one then it means our entry also had a line portion.
                    if len(lp_split) > 1:

                        name = lp_split[0]
                        line = lp_split[1]

                        self.entries.append(
                            {
                                "match": name,
                                "type": "line",
                                "line": line
                            }
                        )

                    # Otherwise, we're either dealing with a whole directory/file ignore entry.
                    else:

                        entry_path_full = os.path.realpath(entry_path_relative)

                        # If our entry is a directory, then we'll ignore the its children
                        if os.path.isdir(entry_path_full):
                            # print('isdir: ' + entry_path_full)

                            self.entries.append(
                                {
                                    "match": entry_path_relative,
                                    "type": "directory",
                                    "line": "N/A"
                                }
                            )

                        # Otherwise the remaining entry is for whole-file ignores
                        elif os.path.isfile(entry_path_full):
                            # print("oh")
                            # print("isfile: " + entry_path_full)

                            self.entries.append(
                                {
                                    "match": entry_path_relative,
                                    "type": "file",
                                    "line": "N/A"
                                }
                            )

            self.file_loaded = True
            return True

        return False


    def __init__(self, target_directory, verbose):
        self.entries = []
        self.path = target_directory + "/.burrowignore"
        self.file_loaded = False
        self.verbose = verbose
        self.load_ignore_file(target_directory)