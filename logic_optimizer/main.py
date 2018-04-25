from string import ascii_letters
from string import digits
from itertools import product
from re import sub

allowed_chars = ascii_letters + digits
operators = "&|^~>="
ops_and_par = operators + "()"
precedence = {"(": 1, ")": 2, "&": 5, "|": 4, "^": 4, "~": 6, ">": 3, "=": 3}


def validate_var(var):
    if var[0] in "01" and len(var) == 1:
        return True
    elif var[0] in digits:
        return False
    else:
        return True


def is_correct(expr):
    prev_is_op = True  # True - oczekiwany nawias ( lub zmienna, False - oczekiwany nawias ) lub operator
    par_count = 0  # licznik nawiasów
    var_end = -1
    for ind, char in enumerate(expr):
        if char in "~ " or ind <= var_end:
            continue
        if prev_is_op:
            if char in allowed_chars:
                if ind > 0 and expr[ind - 1] in allowed_chars:
                    prev_is_char = True
                else:
                    prev_is_char = False
                if not prev_is_char:
                    var_end = ind
                    while var_end < len(expr) - 1 and expr[var_end + 1] in allowed_chars:
                        var_end += 1
                    var = expr[ind:var_end + 1]
                    if not validate_var(var):
                        return False
                prev_is_op = False
            elif char == "(":
                par_count += 1
            else:
                return False
        else:
            if char in operators:
                prev_is_op = True
            elif char == ")":
                par_count -= 1
            else:
                return False
        if par_count < 0:
            return False
    return par_count == 0 and not prev_is_op


def extract_elements(expr):
    expr = expr.replace(' ', '')
    elements = []
    var_end = -1
    for ind, char in enumerate(expr):
        if ind <= var_end:
            continue
        if char in allowed_chars:
            if ind > 0 and expr[ind - 1] in allowed_chars:
                prev_is_char = True
            else:
                prev_is_char = False
            if not prev_is_char:
                var_end = ind
                while var_end < len(expr) - 1 and expr[var_end + 1] in allowed_chars:
                    var_end += 1
                var = expr[ind:var_end + 1]
                elements.append(var)
        if char in ops_and_par:
            elements.append(char)
    return elements


def extract_variables(expr):
    variables = [var for var in extract_elements(expr) if var not in ops_and_par and var not in "01"]
    variables = list(set(variables))
    return variables


def bin_variations(variables):
    bins = ["".join(item) for item in product("01", repeat=len(variables))]
    return bins


def insert_possible_vals(expr):
    variables = extract_variables(expr)
    possible_exprs = []
    for binary in bin_variations(variables):
        e = expr
        for i in range(0, len(binary)):
            e = sub("(?<!\w)" + variables[i] + "(?!\w)", binary[i], e)
        possible_exprs.append(e)
    return possible_exprs


def to_rpn(expr):
    out = []
    stack = []
    for ind, elem in enumerate(extract_elements(expr)):
        i = len(stack) - 1
        if elem == "(":
            stack.append(elem)
        elif elem == ")":
            while i >= 0 and stack[i] != "(":
                out.append(stack.pop())
                i -= 1
            while i >= 0 and stack[i] in operators:
                out.append(stack.pop())
                i -= 1
            stack.pop()
        elif elem in operators:
            if elem == "~":
                while i >= 0 and stack[i] in operators and precedence[stack[i]] > precedence["~"]:
                    out.append(stack.pop())
                    i -= 1
            else:
                while i >= 0 and stack[i] in operators and precedence[stack[i]] >= precedence[elem]:
                    out.append(stack.pop())
                    i -= 1
            stack.append(elem)
        elif elem not in ops_and_par:
            out.append(elem)
    while len(stack) > 0:
        out.append(stack.pop())
    return out


def negate(arg):
    if arg == '1':
        return '0'
    else:
        return '1'


def do_operation(a, b, op):
    if op == '&':
        if a == '1' and b == '1':
            return '1'
        else:
            return '0'
    elif op == "|":
        if a == '1' or b == '1':
            return '1'
        else:
            return '0'
    elif op == "^":
        if a == b:
            return '0'
        else:
            return '1'
    elif op == ">":
        if a == '1' and b == '0':
            return '0'
        else:
            return '1'
    elif op == "=":
        if a == b:
            return '1'
        else:
            return '0'


def evaluate(rpn_expr):
    stack = []
    for elem in rpn_expr:
        if elem in "01":
            stack.append(elem)
        elif elem in operators:
            if elem == "~":
                stack.append(negate(stack.pop()))
            else:
                b = stack.pop()
                a = stack.pop()
                stack.append(do_operation(a, b, elem))
    return stack.pop()


def is_tautology(expr):
    possibilities = insert_possible_vals(expr)
    possibilities = [to_rpn(pos) for pos in possibilities]
    results = [evaluate(pos) for pos in possibilities]
    return '0' not in results


def create_first_table(expr):
    possibilities = insert_possible_vals(expr)
    possibilities = [to_rpn(pos) for pos in possibilities]
    bins = bin_variations(extract_variables(expr))
    table = [bins[ind] for ind, pos in enumerate(possibilities) if (evaluate(pos)) == "1"]
    return table


def group_by_ones(table):
    groups = [[] for i in range(len(table[0]) + 1)]
    for bins in table:
        groups[bins.count("1")].append(bins)
    return groups


def count_differences(a, b):
    diffs = 0
    for ind, letter in enumerate(a):
        if letter != b[ind]:
            diffs += 1
    return diffs


def pair_one_diffs(groups):
    pairs = []
    for ind, group in enumerate(groups):
        if ind < len(groups) - 1:
            for a in group:
                for b in groups[ind + 1]:
                    if count_differences(a, b) == 1:
                        pairs.append([a, b])
    return pairs


def connect_pairs(pairs):
    result = []
    for pair in pairs:
        for i in range(len(pair[0])):
            if pair[0][i] != pair[1][i]:
                new = list(pair[0])
                new[i] = "-"
        result.append("".join(new))
    return result


def group_fours(connected_pairs):
    result = []
    copy = list(connected_pairs)
    while copy:
        found_four = False
        for ind, pair in enumerate(copy):
            if ind > 0 and not found_four:
                if count_differences(copy[0], copy[ind]) == 1:
                    found_four = True
                    result.append([copy.pop(ind), copy.pop(0)])
        if not found_four:
            result.append([copy.pop(0)])
    return result


def connect_fours(fours):
    result = []
    copy = list(fours)
    for ind, f in enumerate(copy):
        if len(f) == 1:
            result.append("".join(copy[ind]))
    copy = [f for f in copy if len(f) > 1]
    result += connect_pairs(copy)
    result = list(set(result))
    for a, gr1 in enumerate(result):
        for b, gr2 in enumerate(result):
            if count_differences(gr1, gr2) == 1:
                if gr1.count('-') > gr2.count('-'):
                    result[b] = result[a]
                else:
                    result[a] = result[b]
    return list(set(result))


def match_binaries(a, b):
    for i in range(len(a)):
        if a[i] != b[i] and a[i] != "-" and b[i] != "-":
            return False
    return True


def prime_imp_chart(expr, connected_fours):
    table = create_first_table(expr)
    result = [["x" if match_binaries(connected_fours[i], table[j]) else "-" for j in range(len(table))] for i in
              range(len(connected_fours))]
    return result


def make_columns_empty(chart, row):
    for i in range(len(chart[row])):
        if chart[row][i] == 'x':
            for j in range(len(chart)):
                if j != row:
                    chart[j][i] = ' '
            chart[row][i] = ' '


def find_essentials(chart):
    result = []
    copy = list(chart)
    finished = False
    while not finished:
        column = -1
        row = -1
        for i in range(len(copy[0])):
            x_in_col = 0
            for j in range(len(copy)):
                if copy[j][i] == 'x':
                    x_in_col += 1
            if x_in_col == 1:
                column = i
                for ind, r in enumerate(copy):
                    if r[column] == 'x':
                        row = ind
        if column >= 0:
            result.append(row)
            make_columns_empty(copy, row)
        else:
            most_xs = 0
            for ind, r in enumerate(copy):
                if r.count('x') > most_xs:
                    row = ind
                    most_xs = r.count('x')
            result.append(row)
            make_columns_empty(copy, row)
        copy[row] = [' ' for c in copy[row]]
        finished = True
        for row in copy:
            for char in row:
                if char != ' ':
                    finished = False
    return result


def back_to_vars(essentials, implicants, variables):
    result = [[] for i in range(len(essentials))]
    for i, num in enumerate(essentials):
        for ind, binary in enumerate(implicants[num]):
            if binary == '0':
                result[i].append("~" + variables[ind])
            if binary == '1':
                result[i].append(variables[ind])
    for ind, variables in enumerate(result):
        result[ind] = " & ".join(variables)
    result = " | ".join(result)
    return result


def quine_mccluskey_algorithm(expr):
    variables = extract_variables(expr)
    table = create_first_table(expr)
    groups = group_by_ones(table)
    pairs = pair_one_diffs(groups)
    connected = connect_pairs(pairs)
    fours = group_fours(connected)
    fours_connected = connect_fours(fours)
    prime_imp = prime_imp_chart(expr, fours_connected)
    essentials = find_essentials(prime_imp)
    simplified = back_to_vars(essentials, fours_connected, variables)
    return simplified


def main():
    print("Podaj wyrazenie logiczne do minimalizacji: ")
    expr = input()
    if is_correct(expr):
        if is_tautology(expr):
            print("Podane wyrazenie jest tautologia")
        else:
            print(quine_mccluskey_algorithm(expr))
    else:
        print("Podane wyrazenie jest niepoprawne")


if __name__ == "__main__":
    main()
