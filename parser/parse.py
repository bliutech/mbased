class Parser:
    '''Parser object for syntax analyses'''

    possible_tokens = [] # This space can hold the definitions of each token
    
    def __init__(self):
        '''Initializes the parser object'''
        print("Initializing the parser")

    def parse(self, tokens : list[str]):
        '''Parses them with the LL(1) grammar and returns any parsing errors'''
        
        parsed_tokens : list[str] = []
        
        if len(tokens) == 0:
            print("Error: No tokens found...")
        elif len(tokens) == 1:
            # check if token is valid and return
        else:
            curr_token_num : int = 0

            # if everything is good, return all the tokens
            return parsed_tokens
