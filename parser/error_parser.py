
ERROR = 0
ASSERTION_ERROR = 1
ATTRIBUTE_ERROR = 2
EOF_ERROR = 3
FLOATINGPOINT_ERROR = 4
GENERATOREXIT = 5
IMPORT_ERROR = 6
INDEX_ERROR = 7
KEY_ERROR = 8
KEYBOARDINTERRUPT = 9
MEMORY_ERROR = 10
NAME_ERROR = 11
NOTIMPLEMENTED_ERROR = 12
OS_ERROR = 13
OVERFLOW_ERROR = 14
REFERENCE_ERROR = 15
RUNTIME_ERROR = 16
STOPITERATION = 17
SYNTAX_ERROR = 18
INDENTATION_ERROR = 19
TAB_ERROR = 20
SYSTEM_ERROR = 21 
SYSTEMEXIT = 22
TYPE_ERROR = 23
UNBOUNDLOCAL_ERROR = 24
UNICODE_ERROR = 25
UNICODEENCODE_ERROR = 26
UNICODEDECODE_ERROR = 27
UNICODETRANSLATE_ERROR = 28
VALUE_ERROR = 29
ZERODIVISION_ERROR = 30

TRACEBACK = 100


import json
import time
from collections import deque

class Scanner(object):
    def __init__(self):
        self.lines = deque()
        self.curr_line = None
        self.words = None

    def append(self, input_stream):
        curr_input = input_stream.split("\n")
        #NOTE can probably change this to extend
        self.lines.append(curr_input[0])    # Just append text not single position array

    def move_to_next_line(self):
        if self.lines:  #Detect if still has item
            self.curr_line = self.lines.popleft()   # get the latest line
        else:
            self.curr_line = None
        self.words = None # Clear out the old words since we are on a new line

    def advance(self):
        # Check if the line has already been split
        if self.words is None:
            if self.curr_line is not None:
                if self.curr_line == "":
                    print("Returning none from advance because curr_line empty")
                    return None # Nothing left to parse
                else:
                    self.words = deque()
                    self.words.extend(self.curr_line.split(" "))
            else:
                print("Returning none from advance because curr_line is None ")
                return None
        
        if self.words:  #Detect is still has item
            print("Getting new word")
            new_word = self.words.popleft()
        else:
            print("Returning none from advance because no more words")
            new_word = None
        
        return new_word

class Parser(object):
    def __init__(self, scanner):
        self.scanner = scanner
    
    def parse(self):
        self.scanner.move_to_next_line()
        new_word = self.scanner.advance()
        while new_word is not None:
            print(new_word)
            new_word = self.scanner.advance()
            if new_word is None:
                self.scanner.move_to_next_line()
                new_word = self.scanner.advance()   
            
        # time.sleep(1)
        # for word in words:
        #     word = word.lower()
        #     if "exception" in word:
        #         return ExceptionToken(line)
        #     elif "traceback" in word:
        #         return TracebackToken(line)
        #     elif "error" in word or word == "generatorerror" or word == "systemexit":
        #         return ErrorToken(word, line)
        #     else:
        #         return UnclassifiedToken(line)

class Token(object):
    def __init__(self, _type, _str):
        self.token_type = _type
        self.token_str = _str

    def get_str(self):
        return self.token_str

    def get_type(self):
        return self.token_type

class ErrorToken(Token):
    def __init__(self, _err_type, _str):
        super().__init__("ERROR" , _str)
        error_type = _err_type

class TracebackToken(Token):
    def __init__(self, _str):
        super().__init__("TRACEBACK" , _str)

class UnclassifiedToken(Token):
    def __init__(self, _str):
        super().__init__("UNCLASSIFIED" , _str)

class ExceptionToken(Token):
    def __init__(self, _str):
        super().__init__("EXCEPTION" , _str)




if __name__ == '__main__':

    scanner = Scanner()
    parser = Parser(scanner)

    in_location = '/home/user/basic_website/test_data/python_errors.json'

    my_data = None
    with open(in_location, 'r') as infile:
        my_data = json.load(infile)

    for data in my_data:
        scanner.append(data["error"])

    parser.parse()




    #     count = 1
    #     for data in json_contents:
    #         print("---------------- {} ----------------".format(count))
    #         my_tokens = scan.scanner(data["error"])
    #         for token in my_tokens:
    #             if token.token_type == "ERROR" or token.token_type == "EXCEPTION":
    #                 print(token.token_str)
    #         print("------------------------------------")
    #         count += 1
