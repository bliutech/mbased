### LL(1) Parsing Table

|       |        var       |       (       | ) |        !        |        &       |        \|       |     $     |
|-------|:-----------------:|:-------------:|:-:|:---------------:|:----------------:|:---------------:|:---------:|
|  Expr | Expr → var Expr' | Expr → (Expr) |   | Expr → NOT Expr |                  |                 |           |
| Expr' |                   |               |   |                 | Expr' → & Expr | Expr' → \| Expr | Expr' → ϵ |

var = Variable \
Expr = Expression

### Backus-Naur Form
```
Expr ::= var Expr'
       | ! Expr
       | ( Expr )
		
Expr' ::= & Expr
        | \| Expr
        | ε

var ::= [A-Z]+
```

### First and Follow Function Table
|       |     FIRST    | FOLLOW |
|-------|:------------:|:------:|
|  Expr | var, !, ( |  $, )  |
| Expr' | &, \|, ε   | $      |
