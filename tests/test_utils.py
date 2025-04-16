from mb8611.utils import parse_table_str


def test_parse_table_str() -> None:
    items = list(parse_table_str('A^B^C^D|+|1^2^3^4|+|5^6^7^8'))
    assert items[0][0] == 'A'
    assert len(items) == 3
    assert items[2][3] == '8'


def test_parse_table_str_different_delim() -> None:
    items = list(parse_table_str('A^B^C^D,1^2^3^4,5^6^7^8', ','))
    assert items[0][0] == 'A'
    assert len(items) == 3
    assert items[2][3] == '8'
