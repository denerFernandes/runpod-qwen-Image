import os
import sys
from huggingface_hub import snapshot_download

print("Downloading Qwen-Image model...")
model_id = "Qwen/Qwen-Image"

# Set cache directory
os.environ["HF_HOME"] = "/app/cache"
os.environ["TRANSFORMERS_CACHE"] = "/app/cache"
os.environ["HF_HUB_CACHE"] = "/app/cache"

try:
    # Create cache directory
    os.makedirs("/app/cache", exist_ok=True)
    
    # Download the model using snapshot_download
    print(f"Downloading {model_id} to /app/cache...")
    snapshot_download(
        repo_id=model_id,
        cache_dir="/app/cache",
        local_dir=f"/app/cache/{model_id.replace('/', '--')}",
        local_dir_use_symlinks=False
    )
    print("Model downloaded successfully!")
except Exception as e:
    print(f"Error downloading model: {e}")
    print("Continuing without pre-downloaded model...")
    # Don't fail the build, just continue without pre-downloaded model
    sys.exit(0)