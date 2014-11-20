#!/bin/sh

file=keywords
save_dir=data
host_name[0]="baidu"
host_name[1]="bing"
url_prefix[0]="http://www.baidu.com/s?wd="
url_prefix[1]="http://cn.bing.com/search?q="
while read keyword
do
    for ((i=0;i<${#host_name[@]};i++))
    do
        path=$save_dir/$keyword/${host_name[$i]}
        if ! [ -e $path ];then
            mkdir -p $path
        fi
        url=${url_prefix[$i]}"$keyword"
        wget --timeout=3 --tries=3 "$url" -O $path/1.htm
    done
done < $file
