import re

def validate_string_input(input_data):
    pattern = r'^[a-zA-Z]+$'  # Regular expression pattern for alphabetic characters
    if re.match(pattern, input_data):
        return True
    else:
        return False