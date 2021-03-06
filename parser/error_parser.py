import json
import time
from collections import deque
import traceback
import sys

# Scanner class for recieving and handling input text
class Scanner(object):
    def __init__(self, debug=False):
        self.debug = debug
        self.lines = deque()
        self.num_lines = 0
        self.num_words = 0
        self.curr_line = None
        self.curr_word = None
        self.words = None
        
        # This is purely for post run debugging
        self.store_input = deque()

    # Appends more input to the scanner stream
    def append(self, input_stream):
        curr_input = input_stream.split("\n")
        self.num_lines = self.num_lines + len(curr_input)
        if self.debug:
            print("DEBUG - Just added {} lines, total {} lines".format(len(curr_input), self.num_lines))
        
        self.store_input.extend(curr_input) 
        self.lines.extend(curr_input)    # Just append text not single position array

    # Moves the scanner selection to the next line
    def move_to_next_line(self):
        if self.lines:  #Detect if still has item
            self.curr_line = self.lines.popleft()   # get the latest line
            self.num_lines -= 1
        else:
            self.curr_line = None
        self.words = None # Clear out the old words since we are on a new line
        if self.debug:
            print("DEBUG - Move to next line. New line contains *{}*".format(self.curr_line))

        if self.curr_line == "":
            self.move_to_next_line()

    # Advances the word pointer one step forward and returns the word
    def advance(self):
        if(self.debug):
            print("DEBUG - Entering advance. Curr word is: *{}* Contents of self.words is: *{}*".format(self.curr_word, self.words ))
        # Check if the line has already been split
        if self.words is None:
            if self.curr_line is not None:
                self.words = deque()
                self.num_words = 0
                self.words.extend(self.curr_line.split())
                self.num_words += len(self.curr_line.split())
            else:
                if(self.debug):
                    print("DEBUG - Returning none from advance because curr_line is None")
                return None
        
        if self.words:  #Detect if still has item
            new_word = self.words.popleft()
            self.num_words -= 1
        else:
            if(self.debug):
                print("DEBUG - Returning none from advance because no more words. Num words left {}".format(self.num_words))
            return None
        
        # Detect if word is an empty string
        if new_word == "":
            if(self.debug):
                print("DEBUG - Got an empty string as a word")
            # new_word = self.advance()   # Dangerous, could end up in an infinite loop here

        if(self.debug):
            print("DEBUG - Returning from advance. New word is *{}* Contents of self.words is *{}*".format(new_word, self.words))

        # mainly for debuggin purposes
        self.curr_word = new_word

        return new_word

    # Enables debug printing
    def set_debug_status(self, status):
        self.debug = status

    # Prints the status of the scanner after finishing up
    def exit_status(self):
        print("DEBUG - Finishing up scanner. Lines left {}".format(self.num_lines))
    
    # Clears the line counter, mainly for debug
    def clear_stats(self):
        self.num_lines = 0


# The parser class uses tree logic in order to parse the input into tokens
class Parser(object):
    def __init__(self, scanner, debug = False):
        self.debug = debug
        self.curr_word = None
        self.scanner = scanner
        self.tokens = deque()
        self.num_unparsed_lines = 0

        # This is for debugging purposes only
        self.unparsed_lines = deque()


    # Begins a loop that will continue to parse until all input has been tokenised
    def parse(self):
        self.scanner.move_to_next_line()
        self.curr_word = self.scanner.advance()
        while self.curr_word is not None:
            if self.curr_word == "Exception":
                self.parse_exception()
            elif self.curr_word == "Traceback":
                self.parse_traceback()
            else:
                if self.debug:
                    print("DEBUG - Could not detect the start of an error in this line. curr_word: *{}* \ncurr_line: {}".format(self.curr_word,self.scanner.curr_line))     
                self.unparsed_lines.append(self.scanner.curr_line)
                self.num_unparsed_lines += 1

            self.scanner.move_to_next_line()
            self.curr_word = self.scanner.advance()
            

    # Sets the debug flag for printing
    def set_debug_status(self, status):
        self.debug = status

    # Returns the parsed tokens
    def get_tokens(self):
        return self.tokens

    # Clears all tokens, mainly for debugging
    def clear_tokens(self):
        self.tokens = deque()

    # Case for parsing an exception token
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

    # Case for parsing a traceback token
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

    # Case for parsing a generic file traceback token
    def parse_file_trace_generic(self):
        full_token_str = self.scanner.curr_line

        self.curr_word = self.scanner.advance()

        # Get file path
        file_path = self.curr_word
        while file_path.count("\"") < 2:   #need to make sure we get whole file location even if there are spaces in the name
            self.curr_word = self.scanner.advance()
            file_path = file_path + self.curr_word
        file_path = file_path.strip(",") #get rid of following comma

        #TODO decide here whether we have a local or library file path

        # Get line number
        self.curr_word = self.scanner.advance() 
        if self.curr_word == "line":
            self.curr_word = self.scanner.advance()
            line_num = self.curr_word.strip(",")
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

        line_str = ""
        if(self.debug):
            print("DEBUG - In parse_file_trace_generic trying to get the line in which the error occured. Curr_line is *{}*".format(self.scanner.curr_line))
        while self.curr_word is not None:
            if line_str == "":
                line_str = self.curr_word
            else:
                line_str = line_str + " " + self.curr_word
            self.curr_word = self.scanner.advance()
        
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
            if ErrorToken.is_standard_error(self.curr_word.strip(":")):
                err_type = self.curr_word.strip(":")
            else:
                err_type = "UnknownError"
            print(err_type)
            self.tokens.append(ErrorToken(err_type, self.scanner.curr_line))   # Implement detection of known error types

        return
    
    # Prints the status on exit 
    def exit_status(self):
        print("DEBUG - Finishing up parser. Number of unparsed lines {}".format(self.num_unparsed_lines))

    # Clears the unparsed line counter. Mainly for debugging
    def clear_stats(self):
        self.num_unparsed_lines = 0 

    # Runs through all of the raw input and compares to the unparsed lines
    # Prints seperators around anything that is unparsed
    def print_unparsed_in_context(self):
        match_started = False

        if self.unparsed_lines:
            curr_unparsed_line = self.unparsed_lines.popleft()
        else:
            curr_unparsed_line = None

        while self.scanner.store_input:
            curr_stored_line = self.scanner.store_input.popleft()
            
            if curr_unparsed_line is not None and curr_unparsed_line in curr_stored_line:
                if not match_started:
                    print("----------------------------------------------------->>")
                    match_started = True
                if self.unparsed_lines:
                    curr_unparsed_line = self.unparsed_lines.popleft()
                else:
                    curr_unparsed_line = None
            elif match_started:
                print("<<-----------------------------------------------------")
                match_started = False

            print(curr_stored_line)

# Generic token object
class Token(object):
    def __init__(self, _type, _str):
        self.token_type = _type
        self.token_str = _str

    def get_str(self):
        return self.token_str

    def get_type(self):
        return self.token_type

# ErrorToken object
class ErrorToken(Token):
    def __init__(self, _err_type, _str):
        super().__init__("ERROR" , _str)
        self.error_type = _err_type
    
    @staticmethod
    def is_standard_error(err_code):
        error_list = ["SystemExit"
                            ,"KeyboardInterrupt"
                            ,"GeneratorExit"
                            ,"Exception"
                            ,"StopIteration"
                            ,"StopAsyncIteration"
                            ,"ArithmeticError"
                            ,"FloatingPointError"
                            ,"OverflowError"
                            ,"ZeroDivisionError"
                            ,"AssertionError"
                            ,"AttributeError"
                            ,"BufferError"
                            ,"EOFError"
                            ,"ImportError"
                            ,"ModuleNotFoundError"
                            ,"LookupError"
                            ,"IndexError"
                            ,"KeyError"
                            ,"MemoryError"
                            ,"NameError"
                            ,"UnboundLocalError"
                            ,"OSError"
                            ,"BlockingIOError"
                            ,"ChildProcessError"
                            ,"ConnectionError"
                            ,"BrokenPipeError"
                            ,"ConnectionAbortedError"
                            ,"ConnectionRefusedError"
                            ,"ConnectionResetError"
                            ,"FileExistsError"
                            ,"FileNotFoundError"
                            ,"InterruptedError"
                            ,"IsADirectoryError"
                            ,"NotADirectoryError"
                            ,"PermissionError"
                            ,"ProcessLookupError"
                            ,"TimeoutError"
                            ,"ReferenceError"
                            ,"RuntimeError"
                            ,"NotImplementedError"
                            ,"RecursionError"
                            ,"SyntaxError"
                            ,"IndentationError"
                            ,"TabError"
                            ,"SystemError"
                            ,"TypeError"
                            ,"ValueError"
                            ,"UnicodeError"
                            ,"UnicodeDecodeError"
                            ,"UnicodeEncodeError"
                            ,"UnicodeTranslateError"
                            ,"Warning"
                            ,"DeprecationWarning"
                            ,"PendingDeprecationWarning"
                            ,"RuntimeWarning"
                            ,"SyntaxWarning"
                            ,"UserWarning"
                            ,"FutureWarning"
                            ,"ImportWarning"
                            ,"UnicodeWarning"
                            ,"BytesWarning"
                            ,"ResourceWarning"]
        return err_code in error_list

    def __str__(self):
        print_str = "{}\n\ttype: {}\n\tstr: {}".format(self.token_type, self.error_type, self.token_str)
        return print_str

# TracebackToken object
class TracebackToken(Token):
    def __init__(self, _str):
        super().__init__("TRACEBACK" , _str)

    def __str__(self):
        print_str = "{}\n\tstr: {}".format(self.token_type, self.token_str)
        return print_str

# GenericFileToken object
class GenericFileToken(Token):
    def __init__(self, _str, _file_path, _line_num, _function_str, _line_str):
        super().__init__("GENERIC_FILE" , _str)
        self.file_path = _file_path
        self.line_num = _line_num
        self.function = _function_str
        self.line = _line_str

    def __str__(self):
        print_str = "{}\n\tfile path: {}\n\tline num: {}\n\tfunction: {}\n\tline: {}".format(self.token_type, self.file_path, self.line_num, self.function, self.line)
        return print_str

# UnclassifiedToken object
class UnclassifiedToken(Token):
    def __init__(self, _str):
        super().__init__("UNCLASSIFIED" , _str)

    def __str__(self):
        print_str = "{}\n\tstr: {}".format(self.token_type, self.token_str)
        return print_str

# ExceptionToken object
class ExceptionToken(Token):
    def __init__(self, _str):
        super().__init__("EXCEPTION" , _str)
    
    def __str__(self):
        print_str = "{}\n\tstr: {}".format(self.token_type, self.token_str)
        return print_str




if __name__ == '__main__':

    scanner = Scanner()
    parser = Parser(scanner)

    in_location = '/home/user/basic_website/test_data/python_errors.json'

    my_data = None
    with open(in_location, 'r') as infile:
        my_data = json.load(infile)

    for data in my_data:
        scanner.append(data["error"])
        try:
            parser.parse()
        except Exception as e:
            print("Exited badly with exception: {}".format(e))
            print("Trying to get full error")
            exc_info = sys.exc_info()
            traceback.print_exception(*exc_info)
            del exc_info
        
        tokens = parser.get_tokens()
        print("****** Got tokens ******")
        for token in tokens:
            print(token)
        print("************************")

        scanner.exit_status()
        parser.exit_status()
        parser.print_unparsed_in_context()
        scanner.clear_stats()
        parser.clear_stats()
        parser.clear_tokens()
        input("Press enter to parse next error")
        
##################### Test scanner is working #####################
    # scanner.set_debug_status(True)
    # scanner.move_to_next_line()
    # curr_word = scanner.advance()
    # still_lines = True
    # while still_lines is True:
    #     curr_line = ""
    #     while curr_word is not None:
    #         curr_line = curr_line + curr_word
    #         curr_word = scanner.advance()

    #     print(curr_line)
    #     scanner.move_to_next_line()
    #     curr_word = scanner.advance()
    #     if curr_word is None:
    #         still_lines = False

###################################################################

####################### Test parser on everything ####################
    # scanner.set_debug_status(True)
    # parser.set_debug_status(True)
    # try:
    #     parser.parse()
    # except Exception as e:
    #     print("Exited badly with exception: {}".format(e))
    #     print("Trying to get full error")
    #     exc_info = sys.exc_info()
    #     traceback.print_exception(*exc_info)
    #     del exc_info
    
    # tokens = parser.get_tokens()
    # for token in tokens:
    #     print("Next token: {}".format(token.get_type()))

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

    scanner.exit_status()
    parser.exit_status()
    parser.print_unparsed_in_context()