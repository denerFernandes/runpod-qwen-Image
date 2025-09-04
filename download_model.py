import torch
from diffusers import DiffusionPipeline
import os

print("Downloading Qwen-Image model...")
model_id = "Qwen/Qwen-Image"

# Set cache directory
os.environ["HF_HOME"] = "/app/cache"
os.environ["TRANSFORMERS_CACHE"] = "/app/cache"
os.environ["HF_HUB_CACHE"] = "/app/cache"

try:
    # Download the model with proper device mapping
    pipe = DiffusionPipeline.from_pretrained(
        model_id,
        torch_dtype=torch.float16,
        device_map="auto",
        trust_remote_code=True,
        cache_dir="/app/cache"
    )
    print("Model downloaded successfully!")
except Exception as e:
    print(f"Error downloading model: {e}")
    # Try alternative download method
    from transformers import AutoModel, AutoTokenizer
    print("Trying alternative download method...")
    tokenizer = AutoTokenizer.from_pretrained(model_id, cache_dir="/app/cache")
    model = AutoModel.from_pretrained(model_id, cache_dir="/app/cache", trust_remote_code=True)
    print("Model components downloaded successfully!")