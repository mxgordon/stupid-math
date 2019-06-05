from sympy.solvers import solve
from sympy import Symbol
from sympy import N
from sympy.parsing.sympy_parser import (parse_expr, standard_transformations, implicit_multiplication)
import multiprocessing
from multiprocessing import Queue


def log(string):
    with open('logs.txt', 'a+') as f:
        f.write(f"{string}/n")
    print(f"Done logging: {string}...")
    return None


def organize():
    start_str = input("> ")
    print(start_str)
    new_str = start_str.split()
    new_str.pop(0)
    equ_str = ""
    variable_bool = False
    varible = None
    for i in new_str:
        if i is None:
            continue
        elif i.lower() == '-v':
            location = new_str.index(i) + 1
            varible = Symbol(new_str[location])
            new_str[location] = None
            variable_bool = True
        else:
            equ_str += i
    if '=' in equ_str:
        equ_str = f"({equ_str})".replace('=', ')-(')
    equ_str = equ_str.replace("^", "**")
    print("Closing organize...")
    return (variable_bool, varible, equ_str)


def solve_equ(variable, equ, q):
    global result
    ans = []
    if variable is None:
        return [f"`{N(equ)}`"]
    else:
        partial_ans = solve(equ, variable, dict=True)
    for i in partial_ans:
        ans.append(f"{variable} = `{N(list(i.values())[0])}`\n")
    print(ans)
    result = ans
    print(result, ans)
    q.put(ans)
    log(ans)
    print("Closing solve_equ...")
    return ans


def parse_shell(equ, q):
    simplified_equ = parse_expr(equ, transformations=standard_transformations + (implicit_multiplication,))
    q.put(simplified_equ)
    log(simplified_equ)
    print("Closing parse shell...")


def fail(reason):
    log(reason)
    quit(reason)


def run(target, queue, args=None, timeout=2):
    proc = multiprocessing.Process(target=target, args=args)
    proc.start()
    proc.join(timeout=timeout)
    if proc.is_alive():
        proc.terminate()
        proc.join()
        fail("too complex! (took >2s to solve)")
    print("Closing run...")
    k = queue.get()
    print('found queue')
    return k


def main():
    queue = Queue()
    # print("a!!!")
    set_pieces = organize()
    final_equ = run(parse_shell, queue, args=(set_pieces[2], queue))
    print('done with run 1')
    queue = Queue()
    answer = run(solve_equ, queue, args=(set_pieces[1], final_equ, queue))
    print('test')
    print(answer)


main()