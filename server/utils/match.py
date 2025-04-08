def normalize_code(code: str) -> str:
    """
    Cleans code by:
    - Stripping whitespace from each line
    - Removing empty lines
    - Removing trailing spaces
    """
    lines = code.splitlines()
    cleaned_lines = [line.strip() for line in lines if line.strip() != ""]
    return "\n".join(cleaned_lines)

def is_solution_match(code: str, solution: str) -> bool:
    """
    Checks if the student's code matches the solution,
    ignoring whitespace, empty lines, and formatting noise.
    """
    return normalize_code(code) == normalize_code(solution)
