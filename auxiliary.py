import re

def clean_input(user_input):
    return re.sub(r'[^\w\s]', '', user_input)