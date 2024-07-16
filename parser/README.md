### LL(1) Parsing Table

|       |        [A-Z]      |       (       | ) |        !        |        &       |        \|       |     $     |
|-------|:-----------------:|:-------------:|:-:|:---------------:|:----------------:|:---------------:|:---------:|
|  Expr | Expr → Var Expr'  | Expr → (Expr) |   |  Expr → ! Expr  |                  |                 |           |
| Expr' |                   |               |   |                 |  Expr' → & Expr  | Expr' → \| Expr | Expr' → ϵ |
|   Var  |   Var → [A-Z]+    |               |   |                 |                  |                 |           |

Var = Variable \
Expr = Expression

### Extended Backus-Naur Form
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
|       |     FIRST    | FOLLOW | NULLABLE |
|-------|:------------:|:------:| -------- |
|  Expr |   [A-Z]+, !, (  |  $, )  |       |
| Expr' |     &, \|    |    $   |    Yes   |
|  Var  |     [A-Z]+   | $, &, \||         |Z
