#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Code for Huffman Coding, Compression and Deconpression.
How to Use: 
compress(text) will output compressed bin data
decompress(bin_data) will output decompress text
Reference: http://bhrigu.me/blog/2017/01/17/huffman-coding-python-implementation/
'''

__author__ = 'szl0834'

from functools import total_ordering
import pickle


@total_ordering
class Node:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    # defining comparators less_than and equals
    def __lt__(self, other):
        return self.freq < other.freq

    def __eq__(self, other):
        if (other == None):
            return False
        if (not isinstance(other, Node)):
            return False
        return self.freq == other.freq


class HuffmanCoding:
    def __init__(self):
        #self.text = text
        self.d_list = []
        self.codes = {}
        self.reverse_mapping = {}

    # function of compression

    def make_frequency_dict(self, text):
        frequency = {}
        for character in text:
            if not character in frequency:
                frequency[character] = 0
            frequency[character] += 1
        return frequency

    def pop_min_value(self, d_list):
        min_index = 0
        for i in range(len(d_list)):
            if d_list[i] < d_list[min_index]:
                min_index = i
        return d_list.pop(min_index)

    def make_node_list(self, frequency):
        for key in frequency:
            node = Node(key, frequency[key])
            self.d_list.append(node)

    def merge_nodes(self):
        while (len(self.d_list) > 1):
            node1 = self.pop_min_value(self.d_list)
            node2 = self.pop_min_value(self.d_list)

            merged = Node(None, node1.freq + node2.freq)
            merged.left = node1
            merged.right = node2

            self.d_list.append(merged)

    def make_codes(self, root=None, current_code=None):
        if (root == None and current_code == None):
            root = self.pop_min_value(self.d_list)
            current_code = ""
            self.make_codes(root, current_code)
        elif (root == None):
            pass
        elif (root.char != None):
            self.codes[root.char] = current_code
            self.reverse_mapping[current_code] = root.char
        else:
            self.make_codes(root.left, current_code + "0")
            self.make_codes(root.right, current_code + "1")

    def get_encoded_text(self, text):
        encoded_text = ""
        for character in text:
            encoded_text += self.codes[character]
        return encoded_text

    def pad_encoded_text(self, encoded_text):
        extra_padding = 8 - len(encoded_text) % 8
        for i in range(extra_padding):
            encoded_text += '0'

        padded_info = "{0:08b}".format(extra_padding)
        encoded_text = "00000000" + "11111111" + padded_info + encoded_text
        return encoded_text

    def get_byte_array(self, padded_encoded_text):
        if (len(padded_encoded_text) % 8 != 0):
            print("Encoded text not padded properly")
            exit(0)

        b = bytearray()
        for i in range(0, len(padded_encoded_text), 8):
            byte = padded_encoded_text[i:i + 8]
            b.append(int(byte, 2))
        return b

    def dumps_codes(self):
        codes = self.reverse_mapping
        dumped_codes = pickle.dumps(codes)
        return dumped_codes

    def compress(self, text):
        #text = self.text
        frequency = self.make_frequency_dict(text)
        self.make_node_list(frequency)
        self.merge_nodes()
        self.make_codes()

        encoded_text = self.get_encoded_text(text)
        padded_encoded_text = self.pad_encoded_text(encoded_text)

        bin_data = self.dumps_codes() + self.get_byte_array(
            padded_encoded_text)
        print("Compressed")
        return bin_data

    # function of decompression

    def get_codes(self, bin_data):
        dumped_codes = bytearray()
        bin_data = bytearray(bin_data)
        codes_index = 0
        for i in range(len(bin_data)):
            if (bin_data[i:i + 2] == b"\x00\xFF"):
                codes_index += 2
                break
            dumped_codes.append(bin_data[i])
            codes_index = i
        pure_bin_data = bin_data[(codes_index + 1):]

        self.reverse_mapping = pickle.loads(dumped_codes)

        return pure_bin_data

    def remove_padding(self, padded_encoded_text):
        padded_info = padded_encoded_text[:8]
        extra_padding = int(padded_info, 2)

        padded_encoded_text = padded_encoded_text[8:]
        encoded_text = padded_encoded_text[:-1 * extra_padding]

        return encoded_text

    def decode_text(self, encoded_text):
        current_code = ""
        decoded_text = ""
        for bit in encoded_text:
            current_code += bit
            if (current_code in self.reverse_mapping):
                character = self.reverse_mapping[current_code]
                decoded_text += character
                current_code = ""

        return decoded_text

    def decompress(self, bin_data):
        bit_string = ""
        pure_bin_data = self.get_codes(bin_data)
        for i in range(len(pure_bin_data)):
            byte = pure_bin_data[i]
            bits = bin(byte)[2:].rjust(8, '0')
            bit_string += bits
        encoded_text = self.remove_padding(bit_string)
        decompressed_text = self.decode_text(encoded_text)
        print("Decompressed")
        return decompressed_text
