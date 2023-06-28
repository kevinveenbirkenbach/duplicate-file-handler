#!/bin/bash

if [ -z "$1" ]
then
    echo "Directory path not provided"
    exit 1
fi

dir="$1"
duplicates=$(find "$dir" -type f -exec md5sum {} + | sort | uniq -d -w32)

if [ -z "$duplicates" ]
then
    echo "No duplicates found."
    exit 0
fi

echo "Duplicates found:"

echo "$duplicates" | while read line
do
    files=$(grep "$line" <<< "$duplicates" | awk '{print $2}')
    file_type=$(file -b --mime-type "${files[0]}")
    if [[ $file_type == text/* ]]
    then
        diff "${files[@]}"
    else
        echo "$files"
    fi
done
