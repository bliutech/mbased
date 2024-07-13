### LL(1) Parsing Table

|       |        term       |       (       | ) |       NOT       |        AND       |        OR       |     $     |
|-------|:-----------------:|:-------------:|:-:|:---------------:|:----------------:|:---------------:|:---------:|
|  Expr | Expr → term Expr' | Expr → (Expr) |   | Expr → NOT Expr |                  |                 |           |
| Expr' |                   |               |   |                 | Expr' → AND Expr | Expr' → OR Expr | Expr' → ϵ |

### Backus-Naur Form
```
Expr ::= term Expr'
       | NOT Expr
       | ( Expr )
		
Expr' ::= AND Expr
        | OR Expr
        | ε

term ::= [A-Z]+
```

### First and Follow Function Table
|       |     FIRST    | FOLLOW |
|-------|:------------:|:------:|
|  Expr | term, NOT, ( |  $, )  |
| Expr' | AND, OR, ε   | $      |
