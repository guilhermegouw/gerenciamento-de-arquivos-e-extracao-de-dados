#!/bin/bash

# Check if the input file and range parameters are provided
if [ $# -ne 3 ]; then
	echo "Usage: $0 input_file min_msgs max_msgs"
	exit 1
fi

input_file=$1
min_msgs=$2
max_msgs=$3

# Check if the input file exists
if [ ! -f "$input_file" ]; then
	echo "Error: File $input_file not found!"
	exit 1
fi

# Check if the range parameters are valid numbers
if ! [[ "$min_msgs" =~ ^[0-9]+$ ]] || ! [[ "$max_msgs" =~ ^[0-9]+$ ]]; then
	echo "Error: min_msgs and max_msgs must be valid numbers!"
	exit 1
fi

# Use awk to filter lines where the number of messages in inbox is within the specified range
awk -v min="$min_msgs" -v max="$max_msgs" '
{
  match($0, /inbox [0-9]+/)
  if (RSTART != 0) {
    msgs = substr($0, RSTART + 6, RLENGTH - 6)
    msgs = msgs + 0
    if (msgs >= min && msgs <= max) {
      print $0
    }
  }
}
' "$input_file"
