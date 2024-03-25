from Stack import Stack
from tokenizer import tokenize


class DivisionByZeroError(Exception):
    pass


class MissingOperandError(Exception):
    pass


class UnknownCharacterError(Exception):
    pass


class MissingOperandOrOperatorError(Exception):
    pass


class InvalidOperand(Exception):
    pass


def get_token_priority(token):
    if token == '(':
        return 0
    if token == '+' or token == '-':
        return 1
    elif token == '/' or token == '*':
        return 2
    elif token == '^':
        return 3


def is_decimal(token):
    try:
        float(token)
        return True
    except ValueError:
        return False


def is_operator(token):
    return token == '+' or token == "-" or token == '/' or token == '^' or token == '*'


def infix_to_postfix(expression):
    stack = Stack()
    list_postfix = []
    list_of_tokens = tokenize(expression)
    print(expression)
    print(list_of_tokens)
    for token in list_of_tokens:
        if token.isdigit() or is_decimal(token):
            list_postfix.append(token)
        elif token == "(":
            stack.push(token)
        elif token == ")":
            while stack.top() != "(" and not stack.is_empty():
                list_postfix.append(stack.pop())
            stack.pop()
        elif is_operator(token):
            current_token_priority = get_token_priority(token)
            while not stack.is_empty() and get_token_priority(stack.top()) >= current_token_priority:
                list_postfix.append(stack.pop())
            stack.push(token)
    while not stack.is_empty():
        list_postfix.append(stack.pop())

    return list_postfix


def calculate(first_operand, second_operand, operator):
    if operator == '+':
        return float(first_operand) + float(second_operand)
    elif operator == '-':
        return float(first_operand) - float(second_operand)
    elif operator == '*':
        return float(first_operand) * float(second_operand)
    elif operator == '/':
        if second_operand == 0:
            raise DivisionByZeroError("Devision by zero.")
        return float(first_operand) / float(second_operand)
    elif operator == '^':
        return float(first_operand) ** float(second_operand)
    else:
        raise InvalidOperand("Invalid operand")


def calculate_postfix(token_list):
    stack = Stack()
    for token in token_list:
        if token.isdigit() or is_decimal(token):
            stack.push(float(token))
        elif is_operator(token):
            if len(stack) < 2:
                raise MissingOperandError("Missing operand for operator.")
            second_operand = stack.pop()
            first_operand = stack.pop()
            result = calculate(first_operand, second_operand, token)
            stack.push(result)
        else:
            raise UnknownCharacterError("Expression contains unsupported character(s).")

    if len(stack) != 1:
        raise MissingOperandOrOperatorError("Missing operand or operator.")
    return stack.pop()


def calculate_infix(expression):
    postfix_expression = infix_to_postfix(expression)
    result = calculate_postfix(postfix_expression)
    return result
