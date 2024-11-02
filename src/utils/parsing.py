import ply.lex as lex
import ply.yacc as yacc

def parse_conditions(condition_str):
    # Define tokens for lexing
    tokens = (
        'AND', 'OR', 'EQ', 'NOTEQ', 'GT', 'LT', 'GTE', 'LTE',
        'LPAREN', 'RPAREN', 'ABS', 'VAR', 'NUMBER', 'STRING', 'MINUS'
    )

    # Regular expressions for simple tokens
    t_AND = r'and'
    t_OR = r'or'
    t_EQ = r'='
    t_NOTEQ = r'<>|!='  # Recognize both <> and != as NOT equal
    t_GT = r'>'
    t_LT = r'<'
    t_GTE = r'>='
    t_LTE = r'<='
    t_LPAREN = r'\('
    t_RPAREN = r'\)'
    t_ABS = r'abs'
    t_MINUS = r'-'

    # Token functions
    def t_VAR(t):
        r'\[[a-zA-Z_][a-zA-Z0-9_]*\]'
        t.value = t.value[1:-1]  # Strip off brackets
        return t

    def t_NUMBER(t):
        r'\d+(\.\d+)?'
        t.value = float(t.value) if '.' in t.value else int(t.value)
        return t

    def t_STRING(t):
        r'\"[^\"]*\"'
        t.value = t.value.strip('"')
        return t

    # Ignore spaces and newlines
    t_ignore = ' \t\n'

    # Error handling for illegal characters
    def t_error(t):
        print(f"Illegal character '{t.value[0]}'")
        t.lexer.skip(1)

    # Build the lexer
    lexer = lex.lex()

    # Data structure to store parsed conditions and intervals
    parsed_data = {}

    # Helper function to add parsed conditions and intervals without logical operators
    def add_condition(variable, operator, threshold):
        if variable not in parsed_data:
            parsed_data[variable] = {"conditions": [], "reference_interval": None}

        # Handle the "not empty" condition with <> ""
        if operator in ['<>', '!='] and threshold == "":
            condition_str = "not empty"
        else:
            condition_str = f"{operator} {threshold}"

        parsed_data[variable]["conditions"].append(condition_str)

        # Calculate numeric reference interval only for numeric conditions
        numeric_conditions = [
            float(cond.split()[1]) for cond in parsed_data[variable]["conditions"]
            if any(op in cond for op in ('<', '<=', '>', '>=')) and cond.split()[1].replace('.', '', 1).isdigit()
        ]

        if len(numeric_conditions) > 1:
            min_threshold, max_threshold = min(numeric_conditions), max(numeric_conditions)
            parsed_data[variable]["reference_interval"] = f"{min_threshold:.1f} < x < {max_threshold:.1f}"

    # Parsing rules
    def p_expression_logical(p):
        '''expression : expression AND expression
                      | expression OR expression'''
        p[0] = f"({p[1]} {p[2]} {p[3]})"

    def p_expression_group(p):
        'expression : LPAREN expression RPAREN'
        p[0] = f"({p[2]})"

    def p_expression_condition(p):
        'expression : condition'
        p[0] = p[1]

    def p_condition_abs(p):
        'condition : ABS LPAREN VAR MINUS VAR RPAREN GT NUMBER'
        var1, var2, threshold = p[3], p[5], p[8]
        abs_condition = f"abs({var1} - {var2}) > {threshold}"
        parsed_data[f"{var1},{var2}"] = {"conditions": [abs_condition], "reference_interval": abs_condition}

    def p_condition_compare(p):
        '''condition : VAR EQ NUMBER
                     | VAR GT NUMBER
                     | VAR LT NUMBER
                     | VAR GTE NUMBER
                     | VAR LTE NUMBER
                     | VAR NOTEQ NUMBER
                     | VAR EQ STRING
                     | VAR NOTEQ STRING'''
        variable, operator, threshold = p[1], p[2], p[3]
        add_condition(variable, operator=operator, threshold=threshold)
        p[0] = f"{variable} {operator} {threshold}"

    # Error handling rule
    def p_error(p):
        if p:
            print(f"Syntax error at '{p.value}'")
        else:
            print("Syntax error at EOF")

    # Build the parser
    parser = yacc.yacc()

    # Parse the input string
    parser.parse(condition_str)

  # Prepare output
    output = {}
    for var, details in parsed_data.items():
        output[var] = {
            "conditions": ', '.join(details['conditions']),
            "reference_interval": details['reference_interval']
        }

    return output