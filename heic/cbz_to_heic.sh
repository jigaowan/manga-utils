#!/bin/zsh
manga_path = $1

tmp_dir=/tmp/mangaheic

unzip_dir=/tmp/mangaheic/unzip
heic_dir=/tmp/mangaheic/heic

if [ ! -d $tmp_dir ]; then
  mkdir $tmp_dir
fi
if [ ! -d $unzip_dir ]; then
  mkdir $unzip_dir
fi
if [ ! -d $heic_dir ]; then
  mkdir $heic_dir
fi

# for file in `find /Volumes/share/books`
find $manga_path -type f | while read -r file; do
  if [ ${file##*.} = "cbz" ]; then
    echo '---------------start-----------------'
    rm -r $unzip_dir/*
    rm -r $heic_dir/*
    echo $(dirname $file)
    echo $(basename $file .cbz)
    ditto -x -k --sequesterRsrc --rsrc $file $unzip_dir
    find $unzip_dir -type f | while read -r img_file; do
      sips -s format heic -s formatOptions 50 $img_file --out $heic_dir
    done
    zip -d "$(dirname $file)/$(basename $file .cbz).zip" "*"
    zip -9 -rjq "$(dirname $file)/$(basename $file .cbz).zip" $heic_dir
    echo '---------------end-------------------'
    # 		echo $(dirname $file)
    # 		echo $(basename $file .cbz)
  fi
done
