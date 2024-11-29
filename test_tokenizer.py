from transformers import AutoTokenizer

# Attempt to load tokenizer
try:
    tokenizer = AutoTokenizer.from_pretrained("google/gemma-2b-it", use_fast=True)
    print("Tokenizer loaded successfully.")
except Exception as e:
    print(f"Error loading tokenizer: {e}")
