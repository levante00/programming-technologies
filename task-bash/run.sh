#!/bin/bash

k=0
s=0
n=0
l=0
for param in "$@"
do

    if [ "$param" = --input_folder ] || [ "$k" -eq 1 ]; then
        if [ "$k" -eq 0 ]; then
        k=1
        continue
        else
        k=0
        input="$param"
        fi
    elif [ "$param" = --extension ] ||[ "$s" -eq 1 ]; then
        if [ "$s" -eq 0 ]
        then
        s=1
        continue
        else
        s=0
        extension="$param"
        fi

    elif [ "$param" = --backup_folder ] || [ "$n" -eq 1 ]; then
        if [ "$n" -eq 0 ]
        then
        n=1
        continue
        else
        n=0
        backup="$param"
        fi
    elif [ "$param" = --backup_archive_name ] || [ "$l" -eq 1 ]; then
        if [ "$l" -eq 0 ]
        then
        l=1
        continue
        else
        l=0
        archive="$param"
        fi
    fi
done

mkdir "$backup" 2> /dev/null
#find "$input" -name \*."$extension" -exec cp {} "$backup" \; 2> /dev/null
find "$input" -name \*."$extension" \
| while read p
  do
  Basename=$(basename ${p%."$extension"})
  mv $p ./$backup/${Basename}${COUNTER}."$extension" 2> /dev/null
  COUNTER=$((COUNTER + 1))
  done
tar -zcf "$archive" ./"$backup" 
echo "done"

