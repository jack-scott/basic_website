
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
        self.lines.extend(curr_input)    # Just append text not single position array

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
                # if self.curr_line == "":
                #     print("Returning none from advance because curr_line empty")
                #     return None # Nothing left to parse
                # else:
                self.words = deque()
                self.words.extend(self.curr_line.split(" "))
            else:
                print("Returning none from advance because curr_line is None ")
                return None
        
        if self.words:  #Detect if still has item
            new_word = self.words.popleft()
        else:
            print("Returning none from advance because no more words")
            return None
        
        # Detect if word is an empty string
        if new_word == "":
            print("Got an empty string as a word")
            # new_word = self.advance()   # Dangerous, could end up in an infinite loop here

        return new_word

class Parser(object):
    def __init__(self, scanner):
        self.curr_word = None
        self.scanner = scanner
        self.tokens = deque()
    
    def parse(self):
        self.scanner.move_to_next_line()
        self.curr_word = self.scanner.advance()
        while self.curr_word is not None:
            if self.curr_word == "Exception":
                self.parse_exception()
            elif self.curr_word == "Traceback":
                self.parse_traceback()
            else:
                print("Could not detect the start of an error. curr_word: *{}* \ncurr_line: {}".format(self.curr_word,self.scanner.curr_line))
                print("Moving to next line")            
                self.scanner.move_to_next_line()
                self.curr_word = self.scanner.advance()

    def get_tokens(self):
        return self.tokens

    def parse_exception(self):
        self.tokens.append(ExceptionToken(self.scanner.curr_line))
        self.scanner.move_to_next_line()
        self.curr_word = self.scanner.advance()
        if self.curr_word == "Traceback":
            self.parse_traceback()
        else:
            print("Problem in parse_exception, expected to see traceback. Instead got curr_word: *{}* \ncurr_line: {}".format(self.curr_word,self.scanner.curr_line))
            #TODO make this break in future

        return

    def parse_traceback(self):
        self.tokens.append(TracebackToken(self.scanner.curr_line))
        self.scanner.move_to_next_line()
        self.curr_word = self.scanner.advance()
        if self.curr_word == "File":
            self.parse_file_trace_generic()
        else:
            print("Problem in parse_traceback, expected to see file. Instead got curr_word: *{}* \ncurr_line: {}".format(self.curr_word,self.scanner.curr_line))
            #TODO make this break in future
        
        return

    def parse_file_trace_generic(self):
        full_token_str = self.scanner.curr_line

        self.curr_word = self.scanner.advance()

        # Get file path
        file_path = self.curr_word
        while file_path.count("\"") < 2:   #need to make sure we get whole file location even if there are spaces in the name
            self.curr_word = self.scanner.advance()
            file_path = file_path + self.curr_word
        file_path = file_path.strip(",")[0] #get rid of following comma

        #TODO decide here whether we have a local or library file path

        # Get line number
        self.curr_word = self.scanner.advance() 
        if self.curr_word == "line":
            self.curr_word = self.scanner.advance()
            line_num = self.curr_word.strip(",")[0]
        else:
            print("Problem in get_file_generic, expected to see line. Instead got curr_word: *{}* \ncurr_line: {}".format(self.curr_word,self.scanner.curr_line))
            line_num = None
        
        # Get function
        self.curr_word = self.scanner.advance() 
        if self.curr_word == "in":
            self.curr_word = self.scanner.advance()
            function_name = self.curr_word
        else:
            print("Problem in get_file_generic, expected to see function name. Instead got curr_word: *{}* \ncurr_line: {}".format(self.curr_word,self.scanner.curr_line))
            function_name = None

        # Get the line in which the error occured
        self.scanner.move_to_next_line()
        self.curr_word = self.scanner.advance()
        line_str = self.curr_word
        while self.curr_word is not None:
            self.curr_word = self.scanner.advance()
            line_str = line_str + self.curr_word
        
        # Extend toke string with the line error
        full_token_str = full_token_str + line_str

        # Push back the file token
        self.tokens.append(GenericFileToken(full_token_str, file_path, line_num, function_name, line_str))

        # Check next line to see if it is another file trace
        self.scanner.move_to_next_line()
        self.curr_word = self.scanner.advance()
        if self.curr_word == "File":
            self.parse_file_trace_generic()
        else:
            self.tokens.append(ErrorToken("not_implemented", self.scanner.curr_line))   # Implement detection of known error types

        print("Succesfully tokenised full error!")
        return


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

class GenericFileToken(Token):
    def __init__(self, _str, _file_path, _line_num, _function_str, _line_str):
        super().__init__("GENERIC_FILE" , _str)
        self.file_path = _file_path
        self.line_num = _line_num
        self.function = _function_str
        self.line = _line_str

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
    
##################### Test scanner is working #####################
    scanner.move_to_next_line()
    curr_word = scanner.advance()
    still_lines = True
    while still_lines is True:
        curr_line = ""
        while curr_word is not None:
            curr_line = curr_line + curr_word
            curr_word = scanner.advance()

        print(curr_line)
        scanner.move_to_next_line()
        curr_word = scanner.advance()
        if curr_word is None:
            still_lines = False
###################################################################

####################### Test parser is working ####################
    # parser.parse()
    # tokens = parser.get_tokens()

    # for token in tokens:
    #     print("Next token: {}  Str: {}".format(token.get_type(), token.get_str()))

###################################################################

    #     count = 1
    #     for data in json_contents:
    #         print("---------------- {} ----------------".format(count))
    #         my_tokens = scan.scanner(data["error"])
    #         for token in my_tokens:
    #             if token.token_type == "ERROR" or token.token_type == "EXCEPTION":
    #                 print(token.token_str)
    #         print("------------------------------------")
    #         count += 1
