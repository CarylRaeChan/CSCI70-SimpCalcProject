class ParserError(Exception):
    pass

# Recursive Descent Parser
class Parser:
    def __init__(self, scanner, output_file): 
        self.scanner = scanner
        self.output_file = output_file
        self.curr = self.scanner.get_token()

    def log(self, msg): # logging helper
        self.output_file.write(msg + '\n') # log message to output file

    def match(self, expected_type): # match helper
        if self.curr.type == expected_type: # if current token matches expected
            self.curr = self.scanner.get_token()
        else:
            self.error(f"{expected_type} expected.")

    def error(self, msg):
        self.log(f"Parse Error: {msg}") # log error message
        raise ParserError("Stop parsing")

    def Prg(self):
        self.Blk()
        if self.curr.type == 'EndofFile': pass # end of file reached
        else: self.error("EndofFile expected.")

    def Blk(self):
        if self.curr.type in ['Identifier', 'Print', 'If']: # start of statement
            self.Stm()
            self.Blk()
        else: pass 

    def Stm(self): # Statement parsing
        if self.curr.type == 'Identifier':
            self.match('Identifier')
            if self.curr.type == 'Assign':
                self.match('Assign')
                self.Exp()
                self.match('Semicolon')
                self.log("Assignment Statement Recognized")
            else:
                self.error("Assign expected.") 

        # Print statement parsing
        elif self.curr.type == 'Print':
            self.match('Print')
            self.match('LeftParen')
            self.Arg()
            self.Argfollow()
            self.match('RightParen')
            self.match('Semicolon')
            self.log("Print Statement Recognized")

        # If statement parsing
        elif self.curr.type == 'If':
            self.log("If Statement Begins") # logging start of If statement
            self.match('If')
            self.Cnd()
            if self.curr.type == 'Colon':
                self.match('Colon')
            else:
                self.error("Colon expected.")
            self.Blk()
            self.Iffollow()
            self.log("If Statement Ends") # logging end of If statement
        else:
            self.error("Identifier, Print, or If expected.")

    # Follow-up parsing for If statement
    def Iffollow(self):
        if self.curr.type == 'Endif':
            self.match('Endif')
            self.match('Semicolon')
        elif self.curr.type == 'Else':
            self.match('Else')
            self.Blk()
            self.match('Endif')
            self.match('Semicolon')
        else:
            self.error("ENDIF or ELSE expected.")

    # Argument parsing for Print statement
    def Arg(self):
        if self.curr.type == 'String': self.match('String')
        else: self.Exp()

    # Follow-up parsing for arguments in Print statement
    def Argfollow(self):
        if self.curr.type == 'Comma':
            self.match('Comma')
            self.Arg()
            self.Argfollow()
        else: pass

    # Expression parsing
    def Exp(self):
        self.Trm() # initial term
        self.Trmfollow() # follow-up terms

    # Follow-up parsing for terms in expression
    def Trmfollow(self):
        if self.curr.type == 'Plus': # addition operator
            self.match('Plus'); self.Trm(); self.Trmfollow()
        elif self.curr.type == 'Minus': # subtraction operator
            self.match('Minus'); self.Trm(); self.Trmfollow()
        else: pass

    # Term parsing
    def Trm(self):
        self.Fac()
        self.Facfollow()

    # Follow-up parsing for factors in term
    def Facfollow(self):
        if self.curr.type == 'Multiply':
            self.match('Multiply'); self.Fac(); self.Facfollow()
        elif self.curr.type == 'Divide':
            self.match('Divide'); self.Fac(); self.Facfollow()
        else: pass

    # Factor parsing
    def Fac(self):
        self.Lit()
        self.Litfollow()

    # Follow-up parsing for literals in factor
    def Litfollow(self):
        if self.curr.type == 'Raise':
            self.match('Raise'); self.Lit(); self.Litfollow()
        else: pass

    # Literal parsing
    def Lit(self):
        if self.curr.type == 'Plus': self.match('Plus'); self.Val()
        elif self.curr.type == 'Minus': self.match('Minus'); self.Val()
        else: self.Val()

    # Value parsing
    def Val(self):
        if self.curr.type == 'Identifier': self.match('Identifier')
        elif self.curr.type == 'Number': self.match('Number')
        elif self.curr.type == 'Sqrt':
            self.match('Sqrt'); self.match('LeftParen'); self.Exp(); self.match('RightParen')
        elif self.curr.type == 'LeftParen':
            self.match('LeftParen'); self.Exp(); self.match('RightParen')
        else: self.error("Identifier, Number, SQRT, or ( expected.")

    def Cnd(self):
        self.Exp()
        self.Rel()
        self.Exp()

    def Rel(self):
        if self.curr.type in ['LessThan', 'Equal', 'GreaterThan', 'LTEqual', 'GTEqual', 'NotEqual']:
            self.match(self.curr.type)
        else:
            self.error("Relational operator expected.")