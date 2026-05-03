from tsp.parser_sol import parser


def solutions(solution_path='./solutions'):

    with open(solution_path, 'r') as set_of_solutions:
        content = set_of_solutions.read()
    
    return parser.parse(content)