from parser.parse import Parser

p: Parser = Parser()
tree = p.parse(["!", "(", "A", "&", "!", "B", "|", "C", ")", "<EOF>"])
print(tree)
