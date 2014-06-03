pdfparser_v.1.6
===============

About
=====

Pdfparser is a simple to use script that seeks out all of the IPS, URLs, and Domains from a PDF, and then converts that into easily readable .csv format. While searching through the document it will seek out both the '.' and '[.]' formats as people sometimes use one variation or the other to sanitize malicous links from accidental clicking.

Usage
======

It is fairly simple to use pdfparser.py. At anytime you can issue a simple '-h' argument to display the help menu
```
$ python pdfparser.py -h
usage: pdfparser.py [-h] [-i | -d | -u | -a] pdf_to_parse csv_to_write

Parses a PDF for URLs, IPs, Domains, or all three at once.

positional arguments:
  pdf_to_parse   Name of PDF to be parsed
  csv_to_write   Name to write to .csv

optional arguments:
  -h, --help     show this help message and exit
  -i, --ips      parse out all ips
  -d, --domains  parse out all domains
  -u, --urls     parse out all urls
  -a, --all      parse out all ips, domains, and urls
```

The optional arguments may only be used one at a time, aka -i is ok, but -id or -i -d are not. At the point where you are searching for two, you might as well search for all three anyway. Sample usage of the search features:
```
$ ./pdfparser.py -i doc_with_info.pdf write_to.csv
$ cat write_to.csv 
5.39.216.227,ip
94.102.63.79,ip
141.255.167.27,ip
5.199.168.152,ip
193.109.68.159,ip
141.255.160.58,ip
5.255.87.146,ip
5.45.181.142,ip

$./pdfparser.py -d doc_with_info.pdf write_to.csv
$cat write_to.csv
222andro[.]net,domain
blockchain.info,domain
encrypted.google.com,domain
sentedcheck[.]net,domain
checksendt[.]net,domain
ekiga.net,domain

$./pdfparser.py -u doc_with_info.pdf write_to.csv
$cat write_to.csv
https://encrypted.google.com,url
http://10.0.0.139/1/post.php,url
http://192.168.1.221/forum/post.php,url
http://192.168.1.9/FUCKERS/post.php,url
http://i5g543itkukkldkt[.]onion/recvdata.php,url

$./pdfparser.py -a doc_with_info.pdf write_to.csv
$cat write_to.csv
5.39.216.227,ip
94.102.63.79,ip
141.255.167.27,ip
5.199.168.152,ip
193.109.68.159,ip
141.255.160.58,ip
5.255.87.146,ip
5.45.181.142,ip
222andro[.]net,domain
blockchain.info,domain
encrypted.google.com,domain
sentedcheck[.]net,domain
checksendt[.]net,domain
ekiga.net,domain
https://encrypted.google.com,url
http://10.0.0.139/1/post.php,url
http://192.168.1.221/forum/post.php,url
http://192.168.1.9/FUCKERS/post.php,url
http://i5g543itkukkldkt[.]onion/recvdata.php,url

```

More to follow soon
===================
