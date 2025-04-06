import sys
import preciceconfigchecker.color as c

def rule_error_message(error: str) -> None:
    """
        This function is the generic shell for an error message, which will result in a system exit.
        It allows specifying an error which will be printed alongside the generic advice.
        :param error: The error which will get printed.
    """
    out: str = c.dyeing("[Error]", c.red) + " Exiting check."
    out += "\n" + error + "."
    out += "\nPlease run \'precice-tools check\' for syntax errors."
    # Link to GitHub issue page
    out += "\n\nIf you are sure this behaviour is incorrect, please leave a report at " + c.dyeing(
        "https://github.com/precice-forschungsprojekt/config-checker/issues", c.cyan)
    sys.exit(out)
