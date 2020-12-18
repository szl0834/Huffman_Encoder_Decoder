#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Code for Testing Huffman Coding
Require project_x.py
Compress test.txt into test.bin
Decompress test.bin into test_decompressed.txt
'''

__author__ = 'szl0834'

from project_x import HuffmanCoding
import re
import sys

def remove_punctuation(text):
    text = text.lower()
    text = re.sub('[^a-z ]+', "", text)
    return text

with open('./test.txt', 'r', encoding='UTF-8') as file:
    text = file.read()
if len(sys.argv) < 2:
    text = remove_punctuation(text)
elif sys.argv[1] != '-all':
    text = remove_punctuation(text)
h = HuffmanCoding()
bin_data = h.compress(text)

with open('./test.bin', 'wb') as output:
    output.write(bin_data)

with open('./test.bin', 'rb') as file:
    bin_data = file.read()
h1 = HuffmanCoding()
decompressed_text = h1.decompress(bin_data)

with open('./test_decompressed.txt', 'w', encoding='UTF-8') as output:
    output.write(decompressed_text)


