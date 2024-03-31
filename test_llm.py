# test_llm.py

import sys
import os

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from model.llm_handler import get_code_from_llm

# The rest of your script...

test_prompt = "Write a Python function to add two numbers:"
generated_code = get_code_from_llm(test_prompt)
print(generated_code)
