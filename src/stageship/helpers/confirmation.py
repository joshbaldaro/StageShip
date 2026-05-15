def confirm(prompt: str) -> bool:
    """
    A simple confirmation prompt that returns True if the user confirms with "y" or "yes", and False otherwise. The
    prompt is case-insensitive and defaults to "No" if the user just presses Enter.

    :param prompt: The confirmation message to display to the user
    :return: True if the user confirms with "y" or "yes", False otherwise
    """
    response = input(f"{prompt} [y/N]: ").strip().lower()
    return response in ("y", "yes")
