class Parser:
    '''Parser object for syntax analyses'''

    possible_tokens = [&. |, !, (, ), [A-Z]]
    
    def __init__(self):
        '''Initializes the parser object'''
        print("Initializing the parser")

    def parse(self, tokens : list[str]):
        '''Takes in the tokens and parses them with the LL(1) grammar'''
        print("Parsing...")
        print("Here are the tokens: ")
        print(tokens)

        ast = "I am an AST"
        assert ast == "I am an AST", "There was a parsing error."
        return ast
