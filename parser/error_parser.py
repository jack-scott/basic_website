
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

class Scanner(object):
    def __init__(self):
        line_num = None
        char_num = None
        curr_char = None
        next_char = None
        input_stream = None

    def scanner(self, input_err):
        input_stream = input_err
        lines = input_stream.split("\n")
        line_num = 1
        char_num = 0
        tokens = []
        for line in lines:
            tokens.append(self.advance(line))
        
        return tokens

    def next_line(self):
        return lines.pop()

    def advance(self, line):
        words = line.split(" ")
        for word in words:
            word = word.lower()
            if "traceback" in word:
                return TracebackToken(line)
            elif "error" in word or word == "generatorerror" or word == "systemexit":
                return ErrorToken(word, line)
            else:
                return UnclassifiedToken(line)



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




if __name__ == '__main__':
    scan = Scanner()
    in_location = '/home/user/basic_website/test_data/python_errors.json'

    with open(in_location, 'r') as infile:
        json_contents = json.load(infile)
        for data in json_contents:
            my_tokens = scan.scanner(data["error"])
            for token in my_tokens:
                if token.token_type == "ERROR":
                    print(token.token_str)