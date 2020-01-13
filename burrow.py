#!/usr/bin/env python3

import argparse
import os
import lib.entropy as entropy
import lib.constants as constants

from binaryornot.check import is_binary
from lib.ignorer import Ignorer
from lib.reporter import Reporter
from pathlib import Path


def print_result(
        match_name,
        filepath,
        filename_match=False,
        multiline=False,
        line="",
        is_outputting_locally=False,
        is_outputting_entropy=False,
        expression_is_entropic=False,
        exact_match=None,
        whole_line="",
        finding_type=""
    ):
    """
    Pretty prints burrow findings onto the terminal.
    """
    
    payload = ""

    # Add the type if we have one
    if finding_type != "":
        payload += "[finding] [" + finding_type + "] | "

    # Add the path of the finding
    payload += match_name + " | " + str(Path(filepath))

    # If we have a specific line, add that on as well
    if not filename_match and not multiline:
        payload += " | line " + str(line)

    # Print the finding surrounded by bars
    print("\n" + "-" * len(payload))
    print(payload)
    print("-" * len(payload))

    # If we have the local output flag set, then also print the exact finding match.
    if is_outputting_locally and whole_line is not "":
        print(whole_line)
        print("-" * len(payload))

    # If we're calculating the entropy,
    if finding_type == "filecontent" and is_outputting_entropy and expression_is_entropic:
        # print(exact_match)
        print("entropy of match: " + str(entropy.calculate(exact_match)))
        print("-" * len(payload))


def go(
        f,
        reporter,
        ignorer,
        is_outputting_locally,
        is_outputting_entropy
    ):

    # Import the regular expression module
    import re

    # Store the path of the target file in a variable
    filename = str(f)

    # By this point we have already removed any files or directories to be ignored from our audit list.
    # This means that at this point, we should only check if a line we're on is to be ignored.

    for expression in constants.ALL_REGEX_CHECKS:
        match_name = expression["name"]
        search_parameters = re.compile(expression["regex"], flags=re.DOTALL|re.IGNORECASE)

        # Are we dealing with the internal contents of a file?
        if expression["type"] == "filecontent":

            try:
                with open(f) as open_file:
                    
                    # Lets look for single-line matches
                    if expression["multiline"] != True:

                        # For each line of a file..
                        for line_number, whole_line in enumerate(open_file):

                            # Check if there is a .burrowignore entry for the line
                            if not ignorer.is_line_ignored(filename, line_number+1):

                                match = re.search(search_parameters, whole_line)

                                if match:

                                    # Save the line as a whole
                                    whole_line = whole_line.rstrip().lstrip()

                                    # Obtain the specific portion of the line that is "secret"
                                    # i.e. if AWS_VAR="x", obtain x
                                    exact_match = match.group("burrow").rstrip().lstrip()

                                    print_result(
                                        match_name,
                                        filename,
                                        line=line_number+1,
                                        is_outputting_locally=is_outputting_locally,
                                        is_outputting_entropy=is_outputting_entropy,
                                        expression_is_entropic=expression["entropic"],
                                        whole_line=whole_line,
                                        exact_match=exact_match,
                                        finding_type=expression["type"]
                                    )

                                    snippet = exact_match[:constants.START_TRUNCATION_LENGTH] + "..." + exact_match[-constants.END_TRUNCATION_LENGTH:]
                                    reporter.add_finding( 
                                        match=match_name,
                                        target_file=filename,
                                        line_number=line_number+1,
                                        snippet=snippet
                                    )

                    # Otherwise, read the entire file as a single stream and search for matching expressions.
                    else:

                        contents = open_file.read()

                        for match in search_parameters.finditer(contents):

                            exact_match = match.group().rstrip()
                            if exact_match:
                                print_result(
                                    match_name,
                                    filename,
                                    multiline=True,
                                    is_outputting_locally=is_outputting_locally,
                                    is_outputting_entropy=is_outputting_entropy,
                                    exact_match=exact_match,
                                    finding_type=expression["type"]
                                )
                                snippet = exact_match.split("\n")[0] + exact_match.split("\n")[1]
                                reporter.add_finding(
                                    match=match_name,
                                    target_file=filename,
                                    line_number="N/A",
                                    snippet=snippet
                                )
            except Exception as ex:
                # We've just tried to open a directory. Woops.
                print(ex)

        # Are we dealing with the name of a file?
        elif expression["type"] == "filename":

            # We'll use match here because we want to start from the beginning of the filename/path
            match = re.match(search_parameters, filename)

            if match:
                print_result(match_name, filename, filename_match=True, finding_type="filename")
                snippet = filename
                reporter.add_finding(
                    match=match_name,
                    target_file=filename,
                    line_number="N/A",
                    snippet=snippet
                )


if __name__ == "__main__":
    # Set up command line arguments
    parser = argparse.ArgumentParser(description="Searches for hardcoded credentials.")
    parser.add_argument(
        "-i",
        "--input-folder",
        help="The directory to scan",
        required=True
    )
    parser.add_argument(
        "-o",
        "--output-folder",
        help="The directory to save burr0w output to",
        default="./burr0w-output.txt"
    )
    parser.add_argument(
        "-v",
        "--verbose",
        help="Enable verbose mode for debugging purposes",
        default=False,
        action="store_true"
    )
    parser.add_argument(
        "--output-local",
        help="Output whole matches to STDOUT. Do not run if logging is in use!",
        default=False,
        action="store_true"
    )
    parser.add_argument(
        "--output-entropy",
        help="Flag used to determine whether the entropy of a match should be outputted",
        default=False,
        action="store_true"
    )
    arguments = parser.parse_args()
    target_directory = arguments.input_folder
    output_directory = arguments.output_folder
    is_outputting_locally = arguments.output_local
    is_verbose = arguments.verbose
    is_outputting_entropy = arguments.output_entropy

    ignorer = Ignorer(target_directory, is_verbose)
    reporter = Reporter(target_directory, output_directory, ignorer, is_verbose)

    print()
    print("burrow - salidas")
    print("version: " + constants.BURROW_VERSION)
    print("target directory: " + os.path.abspath(target_directory))
    print("output file: " + reporter.get_output_file())
    print("in verbose mode: " + str(is_verbose).lower())
    print("outputting entire matches (--output-local): " + str(is_outputting_locally).lower())
    print("outputting entropy calculations (--output-entropy): " + str(is_outputting_entropy).lower())
    print(".burrowignore file present: " + str(ignorer.is_file_loaded()).lower())

    # if is_verbose and ignorer.is_file_loaded():
    print("\nignoring from .burrowignore file:")
    ignorer.pretty_print_list()

    # Obtain all the files in the target directory. Files only, pls.
    target_files = [os.path.join(parent_dir, filename) for parent_dir, child_dirs, filenames in os.walk(target_directory) for filename in filenames]

    target_files = ignorer.remove_ignored_entries(target_files)

    if is_verbose:
        print("\n[verbose] targeting:")
        print("\n- ".join(target_files))

    # Audit all the files!
    for target_file in target_files:
        # If we're not dealing with a binary, then it's all gravy; add it to the list.
        if not is_binary(str(target_file)):
            go(target_file, reporter, ignorer, is_outputting_locally, is_outputting_entropy)

    reporter.output_to_file()
 