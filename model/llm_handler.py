# model/llm_handler.py
from transformers import pipeline, set_seed

# Initialize the pipeline with the chosen model
generator = pipeline('text-generation', model='EleutherAI/gpt-neo-125M')


def get_code_from_llm(prompt):
    # Explicitly set truncation and maximum length for generated text
    generated_text = generator(prompt, max_length=50, truncation=True)[0]['generated_text']
    return generated_text
