#!/bin/bash

# Check if the input file is provided
if [ -z "$1" ]; then
	echo "Usage: $0 input_file [-desc]"
	exit 1
fi

# Check if the input file exists
if [ ! -f "$1" ]; then
	echo "Error: File $1 not found!"
	exit 1
fi

# Check if the second parameter is provided and set the sort order accordingly
if [ -z "$2" ]; then
	sort "$1"
elif [ "$2" == "-desc" ]; then
	sort -r "$1"
else
	echo "Invalid parameter. Use -desc to get the reverse order or no parameter to get the normal order."
	exit 1
fi
