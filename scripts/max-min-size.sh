#!/bin/bash

# Function to find the line with the maximum or minimum size
find_size_line() {
	local file="$1"
	local mode="$2"

	# Initialize variables
	local size=0
	local line=""
	local size_line=""

	# Set initial value based on mode
	if [ "$mode" == "max" ]; then
		size=0
	elif [ "$mode" == "min" ]; then
		size=999999999
	fi

	# Use awk to process the file
	awk -v mode="$mode" -v size="$size" '
  {
    # Extract the size value from the line
    match($0, /size [0-9]+/)
    line_size = substr($0, RSTART + 5, RLENGTH - 5)

    if (mode == "max") {
      if (line_size > size) {
        size = line_size
        size_line = $0
      }
    } else if (mode == "min") {
      if (line_size < size) {
        size = line_size
        size_line = $0
      }
    }
  }
  END {
    print size_line
  }
  ' "$file"
}

# Check if the input file is provided
if [ -z "$1" ]; then
	echo "Usage: $0 input_file [-min]"
	exit 1
fi

# Check if the input file exists
if [ ! -f "$1" ]; then
	echo "Error: File $1 not found!"
	exit 1
fi

# Check if the second parameter is provided
if [ -z "$2" ]; then
	find_size_line "$1" "max"
elif [ "$2" == "-min" ]; then
	find_size_line "$1" "min"
else
	echo "Invalid parameter. Use -min to get the smallest size or no parameter to get the biggest size."
	exit 1
fi
