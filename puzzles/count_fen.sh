#!/bin/bash

# Directory to search files in
DIRECTORY="."

# Iterate through all files in the directory
for file in "$DIRECTORY"/*; do
  if [ -f "$file" ]; then
    # Count the number of lines containing "FEN"
    count=$(grep -c "FEN" "$file")
    # Print the filename and the count
    echo "$file: $count"
  fi
done
