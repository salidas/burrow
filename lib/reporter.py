# -*- coding: utf-8 -*-

class Reporter:


    def is_verbose(self):
        return self.verbose


    def get_output_file(self):
        return self.output_path


    def get_findings(self):
        return self.findings


    def add_finding(
        self,
        match="",
        target_file="",
        line_number="",
        snippet=""
    ):

        # Create a hash to prevent future duplicates
        import hashlib
        prehashed_id = match + ":" + target_file + ":" + str(line_number) + ":" + snippet
        hashed_id = hashlib.sha3_256(prehashed_id.encode('utf-8')).hexdigest()
        if self.is_verbose():
            print("[verbose] prehashed_id: " + prehashed_id)
            print("[verbose] hashed_id: " + hashed_id)

        # I need to check if this finding has been reported already!
        if not any(finding["id"] == hashed_id for finding in self.get_findings()["findings"]):
            if self.is_verbose():
                print("[verbose] this is a new finding; adding it to the list")
        else:
            if self.is_verbose():
                print("[verbose] this is a duplicate. ew!")
    
        finding = {
            "id": hashed_id,
            "match": match,
            "file": target_file,
            "line": line_number,
            "snippet": snippet
        }

        self.findings["findings"].append(finding)
        if self.is_verbose():
            print("[verbose] finding: " + str(finding))


    def output_to_file(self):
        # Create a unique filename. Timestamping should do it
        import json, time

        with open(self.output_path, 'w') as output_file:
            json.dump(self.get_findings(), output_file)


    def generate_output_file_skeleton(self):
        import time
        import lib.constants as constants
        self.findings = {
            # "name": "burr0w",
            "burrow_version": constants.BURROW_VERSION,
            "date": time.strftime("%m-%d-%Y", time.localtime()),
            "time": time.strftime("%H:%M", time.localtime()),
            "target_directory": self.target_directory,
            "findings": [],
            "burrowignore_entries": self.ignorer.get(show_lookup_field=False)
        }


    def __init__(self, target_directory, output_directory, ignorer, verbose=False):
        import os, time

        self.ignorer = ignorer

        self.timestamp = time.strftime("%m%d%y%H%M", time.localtime())

        self.target_directory = os.path.abspath(target_directory)

        self.output_directory = os.path.abspath(output_directory)
        self.output_filename = "results_burrow_output-" + self.timestamp + ".json"

        self.output_path = self.output_directory + "/" + self.output_filename
        # print("\nsaving findings to " + self.output_path)

        self.generate_output_file_skeleton()
        self.verbose = verbose
