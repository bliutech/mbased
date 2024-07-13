test_cases : dict[str, str] = {
    "if (([ebp_1 + 0x14].b == 0 || [ebp_1 + 0x14].b != 0 && [ebp_1 + 0x14].c != 0) || ![ebp_1 + 0x14] == 0) then 387 @ 0x8040da8 else 388 @ 0x8040d8b" : "( ( A | ! A & B ) | ! C )"
    "if ([ebp_1 + 0x14].b == 0 || [ebp_1 + 0x14].b != 0) then 387 @ 0x8040da8 else 388 @ 0x8040d8b" : "( A | ! A )"
    "while (x == 3 && y >= 2):" : "A & B"
    "if ([ebp_1 + 0x14].b == 0 || [ebp_1 + 0x14].b != 0 && [ebp_1 + 0x14].c != 0) || (![ebp_1 + 0x14] == 0) then 387 @ 0x8040da8 else 388 @ 0x8040d8b" : "( A | ! A & B ) | ( ! C )"
}
