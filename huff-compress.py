import sys, getopt, time, array, pickle, re

#==============================================================================
# Load input file and get a sorted node list

class Loader:
    def __init__(self):
        self.frequency = {}
        self.node_list = []
        self.text = ''

    # Load input file by characters
    def load_characters(self):
        sum = 0
        # Open the input file named infile.txt
        with open('infile.txt', 'r') as f:
            for line in f:
                # Store whole file content as a string
                self.text += line
                # Accumulate all characters
                sum += len(line)
                # Compute the frequency of each character and store in frequency dictionary
                for i in range(len(line)):
                    if not line[i] in self.frequency.keys():
                        self.frequency[line[i]] = 1
                    else:
                        self.frequency[line[i]] += 1
        # Add Pseudo-EOF
        self.frequency['|'] = 1
        self.compute_probability(sum)

    # Load input file by words
    def load_words(self):
        sum = 0
        # Open the input file named infile.txt
        with open('infile.txt', 'r') as f:
            for line in f:
                # Store whole file content as a string
                self.text += line
                # Extract all word and other character (numerals, punctuation, white space) as a word in a line
                alphabet = re.findall(r'([A-Za-z]+|[^A-Za-z])', line)
                # Accumulate all words
                sum += len(alphabet)
                # Compute the frequency of each word and store in frequency dictionary
                for word in alphabet:
                    if word not in self.frequency.keys():
                        self.frequency[word] = 1
                    else:
                        self.frequency[word] += 1
        # Add Pseudo-EOF
        self.frequency['|'] = 1
        self.compute_probability(sum)

    # Compute probability for characters or words
    def compute_probability(self, sum):
        for char, count in self.frequency.items():
            # Compute probability
            probability = self.frequency[char] / sum
            if (len(self.node_list) == 0):
                # The first node
                self.node_list.insert(0, Node(char, probability, None, None))
            else:
                # Use 'Binary Search' to sort all leaf nodes
                min = 0
                max = len(self.node_list)-1
                mid = int((min + max)/2)
                while(True):
                    # The probability of the new node is the largest
                    if (probability >= self.node_list[max].getValue()):
                        self.node_list.insert(max+1, Node(char, probability, None, None))
                        break
                    # The probability of the new node is the smallest
                    elif (probability <= self.node_list[min].getValue()):
                        self.node_list.insert(min, Node(char, probability, None, None))
                        break
                    # Find out the correct position to insert the new node
                    elif (min == mid):
                        self.node_list.insert(mid + 1, Node(char, probability, None, None))
                        break
                    else:
                        # Cut and search helf data once for searching
                        if (probability > self.node_list[mid].getValue()):
                            min = mid
                        else:
                            max = mid
                        mid = int((min + max)/2)

    # Get node_list variable
    def getNode_list(self):
        return self.node_list

    # Get test variable
    def getText(self):
        return self.text

#==============================================================================
# Give all symbles their Huffman code using Huffman tree

class Huffman_Tree:
    def __init__(self, node_list):
        self.node_list = node_list
        self.tree = None
        self.code = ''
        t.start('Build tree')
        self.build()
        t.stopPrint('Build tree')
        t.start('Traversal')
        self.huffman_code = self.traversal(self.tree)
        t.stopPrint('Traversal')

    # Build the Huffman tree
    def build(self):
        while(True):
            # Extract the two smallest nodes from sorted node list
            last1 = node_list[0]
            last2 = node_list[1]
            # Add the two probabilities
            value = last1.getValue() + last2.getValue()
            # Remove the two nodes
            node_list.pop(0)
            node_list.pop(0)
            if (len(self.node_list) == 0):
                # Root stored in the tree variable
                self.tree = Node(None, value, last1, last2)
                break
            else:
                # Use 'Binary Search' to search all the nodes for inserting to correct position
                min = 0
                max = len(self.node_list)-1
                mid = int((min + max)/2)
                while(True):
                    # The value of the new node is the largest
                    if (value >= self.node_list[max].getValue()):
                        self.node_list.insert(max+1, Node(None, value, last1, last2))
                        break
                    # The value of the new node is the smallest
                    elif (value <= self.node_list[min].getValue()):
                        self.node_list.insert(min, Node(None, value, last1, last2))
                        break
                    # Find out the correct position to insert the new node
                    elif (min == mid):
                        self.node_list.insert(mid + 1, Node(None, value, last1, last2))
                        break
                    # Cut and search helf data once for searching
                    else:
                        if (value > self.node_list[mid].getValue()):
                            min = mid
                        else:
                            max = mid
                        mid = int((min + max)/2)

    # Recursive function, travesal, traces all the nodes in the Huffman tree through inorder: left -> root -> right
    def traversal(self, root):
        huffman = {}
        # Stop recursion when the root is None
        if root != None:
            self.code += '0'
            # Set the left child node as the new root
            huffman = self.traversal(root.getLeft())
            # Don't store the nodes which aren't the leaves
            if (root.getSymble() != None):
                huffman[root.getSymble()] = self.code

            self.code += '1'
            # Set the right child node as the new root
            right = self.traversal(root.getRight())
            # Combine the huffman dictionary and right dictionary
            huffman.update(right)
        # Delete the extra code and return
        self.code = self.code[:-1]
        return huffman

    # Get huffman_code variable
    def getHuffman_code(self):
        return self.huffman_code

    # Get tree variable
    def getTree(self):
        return self.tree

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
# Compress the whole text to Huffman binary code and export

class Compress:
    def __init__(self, huffman_code, tree, text):
        self.huffman_code = huffman_code
        self.tree = tree
        self.text = text

    # Transfor each character to Huffman code
    def characters_to_code(self):
        all_code = ''
        for i in range(len(self.text)):
            all_code += self.huffman_code[self.text[i]]
        # Add Huffman code of Pseudo-EOF
        all_code += self.huffman_code['|']
        self.compress(all_code)

    # Transfor each word to Huffman code
    def words_to_code(self):
        all_code = ''
        # Use regex to find out all words and other characters in the text
        all_word = re.findall(r'([A-Za-z]+|[^A-Za-z])', self.text)
        for word in all_word:
            all_code += self.huffman_code[word]
        # Add Huffman code of Pseudo-EOF
        all_code += self.huffman_code['|']
        self.compress(all_code)

    # Transfor all character binary code to bytes
    def compress(self, all_code):
        # Calculate the remainder of dividing eight bits
        rest = 8 - (len(all_code) % 8)
        # Fill up the rest bits by character '1'
        for i in range(rest):
            all_code += '1'
        codearray = array.array('B')
        # Store the result of transforing to bytes in codearray
        for i in range(0, len(all_code), 8):
            c = ''
            for j in range(i, i+8):
                c += all_code[j]
            codearray.append(int(c, 2))

        # Export the result to a file
        # f = open('infile.bin', 'wb')
        f = open('huff-compress.bin', 'wb')
        codearray.tofile(f)
        f.close()
        # Export the Huffman tree to a file
        # fh = open('infile-symbol-model.pkl', 'wb')
        fh = open('huff-compress-symbol-model.pkl', 'wb')
        pickle.dump(self.tree, fh)
        fh.close()

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

# Let users enter parameters through command line
opts, args = getopt.getopt(sys.argv[1:], 's:')
opts = dict(opts)

if '-s' in opts:
    if opts['-s'] == 'char':
        t = MyTimer()
        t.start('Build the Huffman tree and code')
        # Load file by character and get node list and text
        loader = Loader()
        loader.load_characters()
        node_list = loader.getNode_list()
        text = loader.getText()
        # Build Huffman tree to gnerate Huffman code
        huffman = Huffman_Tree(node_list)
        huffman_code = huffman.getHuffman_code()
        huffman_tree = huffman.getTree()
        t.stopPrint('Build the Huffman tree and code')
        # Compress whole text to Huffman code and store it
        t.start('Encode the file')
        compress = Compress(huffman_code, huffman_tree, text).characters_to_code()
        t.stopPrint('Encode the file')
    elif opts['-s'] == 'word':
        t = MyTimer()
        t.start('Build the Huffman tree and code')
        # Load file by word and get node list and text
        loader = Loader()
        loader.load_words()
        node_list = loader.getNode_list()
        text = loader.getText()
        # Build Huffman tree to gnerate Huffman code
        huffman = Huffman_Tree(node_list)
        huffman_code = huffman.getHuffman_code()
        huffman_tree = huffman.getTree()
        t.stopPrint('Build the Huffman tree and code')
        # Compress whole text to Huffman code and store it
        t.start('Encode the file')
        Compress(huffman_code, huffman_tree, text).words_to_code()
        t.stopPrint('Encode the file')
    else:
        # Error message
        warning = (
            "*** ERROR: symbol level label (opt: -s LABEL)! ***\n"
            "    -- value (%s) not recognised!\n"
            "    -- must be one of: char / word"
        ) % (opts['-s'])
        print(warning, file=sys.stderr)
