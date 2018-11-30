
import sys, array, pickle, time

#==============================================================================
# Decode

class Decode:
    def __init__(self):
        # load file and reconstruct Huffman tree
        fh = open('huff-compress-symbol-model.pkl', 'rb')
        self.tree = pickle.load(fh)
        fh.close()
        # load the compressed file
        f = open('huff-compress.bin', 'rb')
        file = f.read()
        f.close()
        # Tranfer byte code back to character binary code
        self.all_code = bin(int.from_bytes(file, byteorder='big'))[2:]

    # Get tree variable
    def getTree(self):
        return self.tree

    # Get all_code variable
    def getAll_code(self):
        return self.all_code

#==============================================================================
# Decompress binary code to text

class Decompress:
    def __init__(self, tree, all_code):
        self.tree = tree
        self.all_code = all_code
        text = self.traversal()
        self.output(text)

    # Traces all the nodes in the Huffman tree according to the code
    def traversal(self):
        text = ''
        current = self.tree
        # Trace each character
        for i in range(len(all_code)):
            # Encounter '0' character
            if all_code[i] == '0':
                # Trace its left child node
                current = current.getLeft()
                # Find out the leaf node
                if current.getLeft() == None:
                    symble = current.getSymble()
                    if (symble == '|'):
                        break
                    else:
                        text += symble
                        current = self.tree
            # Encounter '1' character
            else:
                # Trace its right child node
                current = current.getRight()
                # Find out the leaf node
                if current.getRight() == None:
                    symble = current.getSymble()
                    if (symble == '|'):
                        break
                    else:
                        text += symble
                        current = self.tree
        return text

    # Export the decompressed file
    def output(self, text):
        # f = open('infile-decompressed.txt', 'w')
        f = open('huff-compress-decompressed.txt', 'w')
        f.write(text)
        f.close()

#==============================================================================
# Node

class Node:
    def __init__(self, symble, value, left, right):
        self.symble = symble
        self.value = value
        self.left = left
        self.right = right

    def getSymble(self):
        return self.symble

    def getValue(self):
        return self.value

    def getLeft(self):
        return self.left

    def getRight(self):
        return self.right

#==============================================================================
# Timer copied from last assignment

class MyTimer:
    def __init__(self):
        self.startTime = {}

    def start(self, label = None):
        self.startTime[label] = time.clock()

    def stopPrint(self, label = None):
        duration = time.clock() - self.startTime[label]
        msg = 'TIME (%s): %.2f' % (label, duration)
        print(msg, file=sys.stderr)

#==============================================================================
# Main

t = MyTimer()
t.start('Decode the compressed file')
# Load the two file
decode = Decode()
tree = decode.getTree()
all_code = decode.getAll_code()
# Decompress binary code to text
Decompress(tree, all_code)
t.stopPrint('Decode the compressed file')
