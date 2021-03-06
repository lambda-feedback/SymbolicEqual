def evaluation_function(response, answer, params) -> dict:
    """
    Function used to grade a student response.
    ---
    The handler function passes only one argument to evaluation_function(),
    which is a dictionary of the structure of the API request body
    deserialised from JSON.

    The output of this function is what is returned as the API response
    and therefore must be JSON-encodable. This is also subject to
    standard response specifications.

    Any standard python library may be used, as well as any package
    available on pip (provided it is added to requirements.txt).

    The way you wish to structure you code (all in this function, or
    split into many) is entirely up to you. All that matters are the
    return types and that evaluation_function() is the main function used
    to output the grading response.
    """

    from sympy.parsing.sympy_parser import parse_expr
    from sympy import expand, simplify, trigsimp, latex

    # Dealing with special cases that aren't accepted by SymPy
    response, answer = Absolute(response, answer)

    # Safely try to parse answer and response into symbolic expressions
    try:
        res = parse_expr(response)
    except (SyntaxError, TypeError) as e:
        raise Exception("SymPy was unable to parse the response") from e

    try:
        ans = parse_expr(answer)
    except (SyntaxError, TypeError) as e:
        raise Exception("SymPy was unable to parse the answer") from e

    # Add how res was interpreted to the response
    interp = {"response_latex": latex(res)}
    
    # Dealing with special cases
    res, ans = RecpTrig(res, ans)
    res, ans = Decimals(res, ans)

    # Going from the simplest to complex tranformations available in sympy, check equality
    # https://github.com/sympy/sympy/wiki/Faq#why-does-sympy-say-that-two-equal-expressions-are-unequal
    is_correct = bool(res.expand() == ans.expand())
    if is_correct:
        return {"is_correct": True, "level": "1", **interp}

    is_correct = bool(res.simplify() == ans.simplify())
    if is_correct:
        return {"is_correct": True, "level": "2", **interp}

    # Looks for trig identities
    is_correct = bool(res.trigsimp() == ans.trigsimp())
    if is_correct:
        return {"is_correct": True, "level": "3", **interp}

    return {"is_correct": False, **interp}

def RecpTrig(res, ans):
    """
    Reciprocal Trig Functions -> Turn sec, csc, cot into sin form
    
    Parameters
    ----------
    res : SymPy expression
        Reponse Input from Teacher, might have sec, csc, cot
    ans : SymPy expression
        Answer Input from Student, might have sec, csc, cot

    Returns
    -------
    res : SymPy expression
        Updated response input
    ans : SymPy expression
        Updated answer input
        
    Tests
    -----
    Checks if '1+tan(x)**2 + y = sec(x)**2 + y', as this solves the issue
    with sec(x)
    """
    from sympy import sec, csc, cot, sin
    if res.has(sec) or res.has(csc) or res.has(cot):
        res = res.rewrite(sin)
    if ans.has(sec) or ans.has(csc) or ans.has(cot):
        ans = ans.rewrite(sin)
    return res, ans

def Decimals(res, ans):
    """
    Decimals -> Turn into rational form
    Otherwise x/2 not seen as equal to x*0.5
    
    Parameters
    ----------
    res : SymPy expression
        Reponse Input from Teacher, might have decimals
    ans : SymPy expression
        Answer Input from Student, might have decimals

    Returns
    -------
    res : SymPy expression
        Updated response input
    ans : SymPy expression
        Updated answer input
    
    Tests
    -----
    Checks if x*0.5 = x/2
    """
    from sympy import nsimplify
    res = nsimplify(res)
    ans = nsimplify(ans)
    return res, ans

def Absolute(res, ans):
    """
    Accept || as another form of writing modulus of an expression. 
    Function makes the input parseable by SymPy, SymPy only accepts Abs()
    REMARK: this function cannot handle nested || and will raise a 
    SyntaxWarning if more than two | are present in the answer or the 
    response

    Parameters
    ----------
    res : string
        Reponse Input from Teacher, might have ||
    ans : string
        Answer Input from Student, might have ||

    Returns
    -------
    res : string
        Updated response input
    ans : string
        Updated answer input
        
    Tests
    -----
    Checks if Abs(x)+y = |x|+y
    Checks if giving |x+|y|| as response raises a SyntaxWarning
    Checks if giving |x|+|y| as answer raises a SyntaxWarning

    """
    # Response

    n_ans = ans.count('|')
    n_res = res.count('|')
    if n_ans > 2:
        raise SyntaxWarning("Notation in answer might be ambiguous, use Abs() instead of ||","tooMany|InAnswer")
    if n_res > 2:
        raise SyntaxWarning("Notation might be ambiguous, use Abs() instead of ||","tooMany|InResponse")

    # positions of the || values
    abs_pos = [pos for pos, char in enumerate(res) if char == '|']
    res = list(res)
    # for each set of ||
    for i in range(0, len(abs_pos), 2):
        res[abs_pos[i]] = "Abs("
        res[abs_pos[i+1]] = ")"
    res = "".join(res)

    abs_pos = [pos for pos, char in enumerate(ans) if char == '|']
    ans = list(ans)
    for i in range(0, len(abs_pos), 2):
        ans[abs_pos[i]] = "Abs("
        ans[abs_pos[i+1]] = ")"
    ans = "".join(ans)

    return res, ans
