import os
import argparse
import re


# this script will look at a logfile, search for keywords
# if certain words are found, it will add the files listed in the log to a list
# that list will then be used to feed summarizer.py at a later time

# take in a log file as an argument
# take in the string that will be used to extract the file name
parser = argparse.ArgumentParser()
parser.add_argument("-l", "--log-file", type=str, required=True, help="log file to parse")
parser.add_argument("-s", "--search-string", type=str, required=True, help="string to search for in the log file")
parser.add_argument("-c", "--summarize-list", type=str, required=False, help="list of channels to summarize")
parser.add_argument("--summary-location", type=str, required=False, help="location to save the file list to summarize")
args = parser.parse_args()

# make sure search-string has a / at the end
if args.search_string[-1] != "/":
    args.search_string = args.search_string + "/"
search_string = args.search_string

# make sure summary-location has a /
if args.summary_location[-1] != "/":
    args.summary_location = args.summary_location + "/"
summary_location = args.summary_location

# open the log file
with open(args.log_file, "r") as log_file:
    # loop through each line in the log file
    file_list = []
    for line in log_file.readlines():
        # in each line, search for the search string
        if args.search_string in line:
            # if the search string is found, extract everthying from the start of search string to the end of the date
            pattern = f"{search_string}(.*?\\d{{8}})"
            match = re.search(pattern, line)
            if match:
                file_list.append(search_string + match.group(1))
            
# open the summarize_list file and put in python list
channels_to_summarize_list = []
with open(args.summarize_list, "r") as f:
    for channel in f.readlines():
        channels_to_summarize_list.append(channel.strip())


# compare the channels_to_summarize list with the file_list
# if the file_list contains a channel in the channels_to_summarize list, add it to a new list
files_to_summarize = []
for entry in file_list:
    for channel in channels_to_summarize_list:
        if channel in entry:
            files_to_summarize.append(entry)


# need to iterate through the files_to_summarize list and find comlplete file paths that contain that string
# then add those to a new list
complete_file_paths = []
for entry in files_to_summarize:
    # for each entry pull out everything before final slash
    last_slash_index = entry.rfind('/')
    path = entry[:last_slash_index + 1]
    # list all files in the directory "path"
    files_in_path = os.listdir(path)
    #extract all files_in_path that contain the entry
    for file_in_path in files_in_path:
        if entry in path + file_in_path:
            complete_file_paths.append(path + file_in_path)

# write the complete_file_paths to a file
with open(summary_location + "files_to_summarize.txt", "a") as f:
    for entry in list(set(complete_file_paths)):
        print(entry)
        f.write(entry + "\n")
        f.flush()





