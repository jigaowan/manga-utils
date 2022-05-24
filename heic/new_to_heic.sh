#!/bin/zsh
source_file_dir=$1
zipend='.zip'

if [ ! -d $source_file_dir ]; then
  echo $source_file_dir' is not dir'
  exit 1
fi

source_dir=$(dirname $source_file_dir)
# echo $source_dir

source_name=$(basename $source_file_dir)
# echo $source_name

out_file=$source_dir/$source_name$zipend
echo 'out file is '$out_file

if [ -f $out_file ]; then
  echo $out_file' is exist'
  exit 1
fi

tmp_dir=/tmp/mangaheic
heic_dir=/tmp/mangaheic/new

if [ ! -d $tmp_dir ]; then
  mkdir $tmp_dir
fi
if [ ! -d $heic_dir ]
then
mkdir $heic_dir
else
rm -r $heic_dir/*
fi

find $source_file_dir -type f  | while read -r img_file
do
sips -s format heic -s formatOptions 50 $img_file --out $heic_dir
done

zip -9 -rjq $out_file $heic_dir