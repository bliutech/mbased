### LL(1) Parsing Table

|       |        var       |       (       | ) |       NOT       |        AND       |        OR       |     $     |
|-------|:-----------------:|:-------------:|:-:|:---------------:|:----------------:|:---------------:|:---------:|
|  Expr | Expr → var Expr' | Expr → (Expr) |   | Expr → NOT Expr |                  |                 |           |
| Expr' |                   |               |   |                 | Expr' → AND Expr | Expr' → OR Expr | Expr' → ϵ |

var = Variable \
Expr = Expression

### Backus-Naur Form
```
Expr ::= var Expr'
       | NOT Expr
       | ( Expr )
		
Expr' ::= AND Expr
        | OR Expr
        | ε

var ::= [A-Z]+
```

### First and Follow Function Table
|       |     FIRST    | FOLLOW |
|-------|:------------:|:------:|
|  Expr | var, NOT, ( |  $, )  |
| Expr' | AND, OR, ε   | $      |
