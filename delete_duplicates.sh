#!/bin/bash

if [ -z "$1" ]
then
    echo "Directory path not provided"
    exit 1
fi

dir="$1"
duplicates=$(find "$dir" -type f -exec md5sum {} + | sort | uniq -d -w32)

echo "Duplicates found:"

echo "$duplicates" | while read line
do
    files=$(grep "$line" <<< "$duplicates" | awk '{print $2}')
    for file in ${files[@]}
    do
        echo "File: $file"
        echo "Duplicate(s) of this file:"
        for duplicate in ${files[@]}
        do
            if [ $duplicate != $file ]
            then
                echo $duplicate
            fi
        done
        echo "Do you want to delete this file? [y/N]"
        read answer
        if [[ $answer == [yY] || $answer == [yY][eE][sS] ]]
        then
            rm -i "$file"
        fi
    done
done
