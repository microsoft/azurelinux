#!/bin/bash

# Function to display script usage
usage() {
    echo "Usage: $0 directory annotation"
    echo "Example: $0 ./project-directory Nullable"
    exit 1
}

# Function to remove Java annotations and corresponding imports
remove_java_annotations() {
    local directory="$1"
    local annotation="$2"
    # Find all .java files in the directory
    find "$directory" -type f -name "*.java" -print0 | while IFS= read -r -d '' file; do
        # Check if the file is readable
        if [ -r "$file" ]; then
            echo "Processing: $file"
            # Remove annotations without arguments
            sed -i -E "s/@($annotation)\(\s*\)//g" "$file"
            # Remove annotations with arguments
            sed -i -E "s/@($annotation)\([^()]*(\([^()]*\)[^()]*)*\)//g" "$file"
            # Remove errorprone annotations without arguments
            sed -i -E "s/@(com\.google\.errorprone\.annotations\.$annotation)\(\s*\)//g" "$file"
            # Remove errorprone annotations with arguments
            sed -i -E "s/@(com\.google\.errorprone\.annotations\.$annotation)\([^()]*(\([^()]*\)[^()]*)*\)//g" "$file"
            # Remove imports of classes with annotations
            sed -i -E "/^import .*\.($annotation);$/d" "$file"
        else
            echo "Error: Cannot read file $file"
        fi
    done
}

# Check if there are exactly two arguments
if [ "$#" -ne 2 ]; then
    usage
fi

# Check if the directory exists
if [ ! -d "$1" ]; then
    echo "Error: Directory '$1' not found."
    exit 1
fi

# Check if the directory is readable
if [ ! -r "$1" ]; then
    echo "Error: Directory '$1' is not readable."
    exit 1
fi

# Check if the annotation is provided
if [ -z "$2" ]; then
    echo "Error: Annotation not provided."
    usage
fi

remove_java_annotations "$1" "$2"