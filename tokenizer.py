import re

REGEX = r'(?:\d*\.\d+)|(?:\d+)|(?:[()+\-\^/*])'


class ExpressionNotStringError(Exception):
    pass


class UnknownCharacterError(Exception):
    pass


class ConsecutiveOperatorsError(Exception):
    pass


class ConsecutiveOperandError(Exception):
    pass


class NoOperatorError(Exception):
    pass


class NoOperandError(Exception):
    pass


class InvalidBracketsError(Exception):
    pass


class DivisionByZeroError(Exception):
    pass


class MissingOperandError(Exception):
    pass


def is_decimal(token):
    try:
        float(token)
        return True
    except ValueError:
        return False


def tokenize(expression):
    if not isinstance(expression, str):
        raise ExpressionNotStringError("Expression should be string!")

    tokens = re.findall(REGEX, expression)

    if expression.replace(" ", "") != "".join(tokens):
        raise UnknownCharacterError("Expression contains unsupported character(s).")

    i = 0
    while i < (len(tokens) - 1):
        if tokens[i] in ['+', '-', '^', '*', '/'] and tokens[i + 1] in ['+', '-', '^', '*', '/']:
            raise ConsecutiveOperatorsError("Two adjacent operators detected.")
        i += 1

    i = 0
    while i < (len(tokens) - 1):
        is_first_token_number = tokens[i].isdigit() or is_decimal(tokens[i])
        is_second_token_number = tokens[i + 1].isdigit() or is_decimal(tokens[i + 1])
        if is_first_token_number and is_second_token_number:
            raise ConsecutiveOperandError("Two adjacent operands detected.")
        i += 1

    filtered_tokens = []
    next_unary = True
    i = 0
    while i < len(tokens):
        token = tokens[i]
        if token == '-' and next_unary:
            if i + 1 < len(tokens):
                next_token = tokens[i + 1]
                if next_token[0].isdigit():
                    filtered_tokens.append("-" + next_token)
                    i += 2
                    next_unary = False
                    continue
                else:
                    filtered_tokens.append(token)
            else:
                filtered_tokens.append(token)
        elif token.isdigit():
            filtered_tokens.append(token)
            next_unary = False
        elif token == '(':
            filtered_tokens.append(token)
            next_unary = True
        else:
            filtered_tokens.append(token)
        i += 1

    br = 0
    for token in filtered_tokens:
        if token == '(':
            br += 1
        elif token == ')':
            br -= 1
        if br < 0:
            break
    if br != 0:
        raise InvalidBracketsError("Invalid brackets")

    operand = False
    operator = False
    for token in filtered_tokens:
        if token in ['+', '-', '^', '*', '/']:
            operator = True
        if token.isdigit() or is_decimal(token):
            operand = True

    if not operator:
        raise NoOperatorError("There is no operator in expression.")
    if not operand:
        raise NoOperandError("There is no operand in expression.")

    i = 0
    while i < (len(filtered_tokens) - 1):
        if filtered_tokens[i] == '/' and filtered_tokens[i + 1] == '0':
            raise DivisionByZeroError("Division by Zero")
        i += 1

    i = 0
    while i < len(filtered_tokens) - 1:
        current_token = filtered_tokens[i]
        next_token = filtered_tokens[i + 1]
        if (current_token in ['+', '-', '^', '*', '/'] and
                (not (next_token.isdigit() or is_decimal(next_token) or next_token == '('))):
            raise MissingOperandError("Missing operand after operator.")
        i += 1
    if filtered_tokens[-1] in ['+', '-', '^', '*', '/']:
        raise MissingOperandError("Missing operand after operator.")

    list_of_tokens = []
    if filtered_tokens[1].startswith('-'):
        for i in range(len(filtered_tokens)):
            if i == 1 and filtered_tokens[i - 1] != '(':
                list_of_tokens.append("-")
                list_of_tokens.append(filtered_tokens[i][1:])
            else:
                list_of_tokens.append(filtered_tokens[i])
    else:
        list_of_tokens = filtered_tokens

    return list_of_tokens


if __name__ == '__main__':
    #
    # key: izraz, value: očekivana lista tokena
    #
    test_cases = {
        # test floats
        "-20*7.9/(3-7)": ['-20', '*', '7.9', '/', '(', '3', '-', '7', ')'],
        "(2.08-.03) ^ 2": ['(', '2.08', '-', '.03', ')', '^', '2'],
        "2+(3*4)": ['2', '+', '(', '3', '*', '4', ')'],
        # "22     56": ['22', '56'],
        "1.5 * (6 - (3.5 / 2))": ['1.5', '*', '(', '6', '-', '(', '3.5', '/', '2', ')', ')'],
        "3 + 4 - 5 * (6 / 2)": ['3', '+', '4', '-', '5', '*', '(', '6', '/', '2', ')'],
        "2^3 * 4 - 6 / 2": ['2', '^', '3', '*', '4', '-', '6', '/', '2'],
        "10 + (5 * 2 - (3 / 1))": ['10', '+', '(', '5', '*', '2', '-', '(', '3', '/', '1', ')', ')'],
        #"-1 * (-2 + 3) - (4 / (-2))": ['-1', '*', '(', '-2', '+', '3', ')', '-', '(', '4', '/', '(', '-2', ')' ')'],
        "3.14 * (2 + 3.14) / 2": ['3.14', '*', '(', '2', '+', '3.14', ')', '/', '2'],
        #"(-3.14 * (-2))": ['(', '-3.14', '*', '-2', ')'],
        " 6.11 - 74 * 2": ['6.11', '-', '74', '*', '2'],
        " 6.11 - 74/2": ['6.11', '-', '74', '/', '2'],
        " 6.11 + 74/2": ['6.11', '+', '74', '/', '2'],
        "(4.2 + 3) * (5 - 2.5)": ['(', '4.2', '+', '3', ')', '*', '(', '5', '-', '2.5', ')'],
        "3 * 4 ^ (2 + 1)": ['3', '*', '4', '^', '(', '2', '+', '1', ')'],
        "5 * (3 + (2 * 4))": ['5', '*', '(', '3', '+', '(', '2', '*', '4', ')', ')'],
        "12 / 3 - (8 / 2)": ['12', '/', '3', '-', '(', '8', '/', '2', ')'],
        #"3 + (-4) * (7 / 2)": ['3', '+', '-4', '*', '(', '7', '/', '2', ')'],
        #"-2 + (4 * (-3))": ['-2', '+', '(', '4', '*', '-3', ')'],
        #"1 + (-2) - 3 * (-4) + 5": ['1', '+', '-2', '-', '3', '*', '-4', '+', '5'],
        "6 / (2 + 3) - (4 + 5 * 3)": ['6', '/', '(', '2', '+', '3', ')', '-', '(', '4', '+', '5', '*', '3', ')'],
        #"2.5 + (-4.2) * (7.8 / 2)": ['2.5', '+', '-4.2', '*', '(', '7.8', '/', '2', ')'],
        "-2.7 * (3.5 - (2.1 / 4))": ['-2.7', '*', '(', '3.5', '-', '(', '2.1', '/', '4', ')', ')']

        # test invalid
        # "ab cd": [],
        # "10,22": ['10', '22']

    }

    for expression, expected_tokens in test_cases.items():
        tokens = tokenize(expression)
        print(f"Izraz: '{expression}', Rezultat: {tokens}")
        assert tokens == expected_tokens
