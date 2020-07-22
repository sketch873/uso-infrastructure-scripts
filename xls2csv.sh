#!/bin/bash

if [ $# -ne 1 ] || [ ! -d "$1" ]; then
	echo "Usage: $0 DIR_DATA" 1>&2
	exit 1
fi

pushd "$1" &> /dev/null
IFS=$'\n'
for file in *.xls; do
	csv_file=$(basename "$file" .xls).csv
	echo "Convert $file to $csv_file"
	ssconvert "$file" "$csv_file" &> /dev/null
done
popd &> /dev/null
