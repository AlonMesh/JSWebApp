def normalize_code(code: str) -> str:
    """
    Cleans code by:
    - Removing comments starting with //
    - Stripping whitespace from each line
    - Removing empty lines
    """
    lines = code.splitlines()
    cleaned_lines = []

    for line in lines:
        # Remove comments starting with //
        if '//' in line:
            line = line.split('//', 1)[0]

        line = line.strip()
        if line:
            cleaned_lines.append(line)

    return "\n".join(cleaned_lines)

def is_solution_match(code: str, solution: str) -> bool:
    """
    Checks if the student's code matches the solution,
    ignoring whitespace, empty lines, and formatting noise.
    """
    return normalize_code(code) == normalize_code(solution)
