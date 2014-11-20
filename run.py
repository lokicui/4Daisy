#encoding=utf8
import os
import sys
import re
import pdb
import urllib
import urllib2


def crawel_bing(query, save_dir='data', page=10):
    '''
    爬取bing并保存百度的一个搜索结果页面
    保存目录为 save_dir/query/bing/pagenum.htm
    '''
    path = '%s/%s/bing' % (save_dir, query)
    if not os.path.isdir(path):
        os.makedirs(path)
    encoded_query =  urllib.quote(query)
    host = 'http://cn.bing.com'
    url = '%s/search?q=%s' % (host, encoded_query)
    next_url_pattern = re.compile(r'<li><a href="(/search[^\"]+?)" class="sb_pagN" title="', re.I)
    for i in range(0, page):
        encoded_query =  urllib.quote(query)
        response = urllib2.urlopen(url, timeout=3)
        content = response.read()
        fname = '%s/%d.htm' % (path, i + 1)
        open(fname, 'w').write(content)
        m = next_url_pattern.search(content)
        if not m:
            break
        url = m.group(1)
        url = '%s%s' % (host, url.replace('&amp;', '&'))


def crawel_baidu(query, save_dir='data', page=10):
    '''
    爬取baidu并保存百度的一个搜索结果页面
    保存目录为 save_dir/query/baidu/pagenum.htm
    '''
    path = '%s/%s/baidu' % (save_dir, query)
    if not os.path.isdir(path):
        os.makedirs(path)
    url_pattern = 'http://www.baidu.com/s?wd=%s&pn=%d'
    for i in range(0, page):
        encoded_query =  urllib.quote(query)
        url = url_pattern % (encoded_query, i * 10)
        response = urllib2.urlopen(url, timeout=3)
        fname = '%s/%d.htm' % (path, i + 1)
        open(fname, 'w').write(response.read())


def print_usage():
    print 'Usage:\n\tpython %s keywords' % sys.argv[0]

def main():
    if len(sys.argv) != 2:
        print_usage()
        sys.exit(-1)

    fname = sys.argv[1]
    if not os.path.isfile(fname):
        print "keywords[%s] dones't exists" % fname
        sys.exit(-2)

    for line in open(fname):
        crawel_baidu(line.strip())
        crawel_bing(line.strip())

if __name__ == '__main__':
    main()
