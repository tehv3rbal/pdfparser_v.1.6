#!/usr/bin/env python

from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfdevice import PDFDevice
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from StringIO import StringIO
import argparse
import requests
import os.path
import re
import sys
import csv


'''
    This script takes a PDF document and parses through looking for IP's, URL's and Domain names to extract either individually, or all three at once.
    All of the output is written to .csv format. The search of TLD's finds both TLD's and gTLD's to parse out. It will also 
    compensate for different notations, searching for both '.' and '[.]' formats (the [.] is used to sanitize malicous web sites in order to prevent
    accidental clicking) in documentation. When the script is first ran, it searches to see if there is a file called "cached_tlds.txt" in the same directory where the 
    script is located, and if there is not one, it will then make a request to the TLD list from publicsuffix.org and create the file to be cached. 
    After this, all of the domain searches will come from this list, making it usuable offline. To update the TLD list, simply delete 
    the "cached_tlds.txt" file and it will be regenerated when the script is ran.   

'''
def main(argv):
    
    parser = argparse.ArgumentParser(description="Parses a PDF for URLs, IPs, Domains, or all three at once.", prog="pdfparser.py")
    parser.add_argument("pdf_to_parse", help="Name of PDF to be parsed")
    parser.add_argument("csv_to_write", help="Name to write to .csv")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-i", "--ips", help="parse out all ips", action="store_true")
    group.add_argument("-d", "--domains", help="parse out all domains", action="store_true")
    group.add_argument("-u", "--urls", help="parse out all urls", action="store_true")
    group.add_argument("-a", "--all", help="parse out all ips, domains, and urls", action="store_true")
    args = parser.parse_args()
    
    txt = convert_pdf_to_text(args.pdf_to_parse)
    outputfile = args.csv_to_write
    tld = check_for_cached_tlds()
    ips = []
    urls = []
    doms = []
    
    
  
    if args.ips:
        ips = find_ips(txt, outputfile)
    elif args.domains:
        doms = find_domains(txt, outputfile, tld)
    elif args.urls:
        urls = find_urls(txt, outputfile)
    elif args.all:
        ips = find_ips(txt, outputfile)
        doms = find_domains(txt, outputfile, tld)
        urls = find_urls(txt, outputfile)
    else:
        print ("\nusage: pdfparser.py [-h] [-i | -d | -u | -a] pdf_to_parse csv_to_write")
        print ("pdfparser.py: error: no options given")
    
   
    with open(outputfile, 'w') as f:
        writer = csv.writer(f)
        for ip in ips:
            writer.writerow((ip,'ip')) 
        for dom in doms:
            writer.writerow((dom,'domain'))
        for url in urls:
            writer.writerow((url, 'url'))
            
        
   
   
          
def convert_pdf_to_text(path):
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    fp = open(path, 'rb')
    device = TextConverter(rsrcmgr, retstr,  codec=codec, laparams=laparams)
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    password = ""
    maxpages = 0
    caching = True
    pagenos=set()
    for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password, caching=caching, check_extractable=True):
        interpreter.process_page(page)
    fp.close()
    device.close()
    str = retstr.getvalue()
    retstr.close()
    return str


def check_for_cached_tlds():
     if os.path.isfile('cached_tlds.txt'):
        with open('cached_tlds.txt', 'r') as c:
            tld = c.readlines()
            tld = [w.replace('\n','') for w in tld]
        return tld
     else:
        tld = []
        with open('cached_tlds.txt', 'w') as f:
            r = requests.get(r'https://publicsuffix.org/list/effective_tld_names.dat')
            r = r.text
            doc = r.split('\n')
            tlds = []
            pattern = re.compile(r'^(?:\w*|\.\w*|\*\.\w*)(?!\.)$\b', re.I)
            for lines in doc:
                line = re.findall(pattern, lines)
                for item in line:    
                    if item not in tlds:
                        tlds.append(item)
            tlds = [w.replace('.','') for w in tlds]
            tlds = [w.replace('*','') for w in tlds]
            for item in tlds:
                f.write("%s\n" % item)
        return tlds

def find_ips(txt, outputfile):
    lines = txt.split('\n')
    ips = []
    pattern = re.compile(r'(?:[\d]{1,3})\.(?:[\d]{1,3})\.(?:[\d]{1,3})(?:\.|\[\.\])(?:[\d]{1,3})', re.I)
    for line in lines:
        line = line.rstrip()
        results = re.findall(pattern, line)
        for item in results:
            if item not in ips:
                ips.append(item)
    return ips
    
def find_urls(txt, outputfile):
    lines = txt.split('\n')
    urls = []
    pattern = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', re.I)
    for line in lines:
        line = line.rstrip()
        results = re.findall(pattern, line)
        for item in results:
            if item not in urls:
                urls.append(item)
    return urls
   
def find_domains(txt, outputfile, tld):
    lines = txt.split('\n')
    domains = []
    pattern = re.compile(r'\b((?!www(?:\.|\[\.\]))(?:\w+(?:\.|\[\.\]))+(?:%s))\b' % "|".join(tld)) 
    for line in lines:
        line  = line.rstrip()
        results  = re.findall(pattern, line)
        for item in results:
            if item not in domains:
                domains.append(item)
    return domains
    
if __name__ == "__main__":
    main(sys.argv[1:])

