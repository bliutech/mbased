### Extended Backus-Naur Form (EBNF) Grammar
An EBNF context-free grammar (CFG) representing a formal language for boolean expressions.

```
Expr ::= Term Expr'

Expr' ::= | Expr'
        | & Expr'
        | ^ Expr'
        | ε

Term ::= ( Expr )
        | ! Term
        | Var

Var ::= [A-Z]+
        | t
        | f
```

### LL(1) Parse Table
The parse table applying all of the above production rules in the EBNF grammar showing that it is LL(1).

TODO: Update this table.

|       |        [A-Z]      |       (       | ) |        !        |        &       |        \|       |     $     |
|-------|:-----------------:|:-------------:|:-:|:---------------:|:----------------:|:---------------:|:---------:|
|  Expr | Expr → Var Expr'  | Expr → (Expr) |   |  Expr → ! Expr  |                  |                 |           |
| Expr' |                   |               |   |                 |  Expr' → & Expr  | Expr' → \| Expr | Expr' → ϵ |
|   Var  |   Var → [A-Z]+    |               |   |                 |                  |                 |           |

### First and Follow Function Table
A table showing the FIRST and FOLLOW sets of each non-terminal in the EBNF grammar along with if the non-terminal is NULLABLE.

TODO: Update this table.

|       |     FIRST    | FOLLOW | NULLABLE |
|-------|:------------:|:------:| :-------: |
|  Expr |   [A-Z]+, !, (  |  $, )  |       |
| Expr' |     &, \|    |    $   |    Yes   |
|  Var  |     [A-Z]+   | $, &, \||         |Z
