### LL(1) Parsing Table

|       |        [A-Z]      |       (       | ) |        !        |        &       |        \|       |     $     |
|-------|:-----------------:|:-------------:|:-:|:---------------:|:----------------:|:---------------:|:---------:|
|  Expr | Expr → Var Expr'  | Expr → (Expr) |   |  Expr → ! Expr  |                  |                 |           |
| Expr' |                   |               |   |                 |  Expr' → & Expr  | Expr' → \| Expr | Expr' → ϵ |
|   Var  |   Var → [A-Z]+    |               |   |                 |                  |                 |           |

Var = Variable \
Expr = Expression

### Backus-Naur Form
```
Expr ::= Var Expr'
       | ! Expr
       | ( Expr )
		
Expr' ::= & Expr
        | \| Expr
        | ε

Var ::= [A-Z]+
```

### First and Follow Function Table
|       |     FIRST    | FOLLOW |
|-------|:------------:|:------:|
|  Expr |   [A-Z]+, !, (  |  $, )  |
| Expr' |   &, \|, ε   |    $   |
|  Var  |     [A-Z]+   | $, &, \||
