import runpod
import torch
from diffusers import DiffusionPipeline
import base64
from io import BytesIO
from PIL import Image
import os

# Global variables for model caching
pipe = None
device = None
torch_dtype = None

def load_model():
    """Load the Qwen-Image model pipeline from pre-downloaded cache"""
    global pipe, device, torch_dtype
    
    model_name = "Qwen/Qwen-Image"
    cache_dir = "/app/cache"
    
    # Determine device and dtype
    if torch.cuda.is_available():
        torch_dtype = torch.bfloat16
        device = "cuda"
    else:
        torch_dtype = torch.float32
        device = "cpu"
    
    print(f"Loading model on {device} with dtype {torch_dtype} from cache...")
    
    try:
        # Load the pipeline from cache
        pipe = DiffusionPipeline.from_pretrained(
            model_name, 
            torch_dtype=torch_dtype,
            cache_dir=cache_dir,
            local_files_only=True  # Only use cached files
        )
        pipe = pipe.to(device)
        print("Model loaded successfully from cache!")
        
    except Exception as e:
        print(f"Error loading model from cache: {e}")
        print("Falling back to online download...")
        # Fallback to online download if cache fails
        pipe = DiffusionPipeline.from_pretrained(
            model_name, 
            torch_dtype=torch_dtype,
            cache_dir=cache_dir
        )
        pipe = pipe.to(device)
        print("Model loaded successfully with fallback!")

def generate_image(job):
    """Generate image based on the input job"""
    global pipe
    
    try:
        # Get job input
        job_input = job["input"]
        
        # Extract parameters with defaults
        prompt = job_input.get("prompt", "")
        negative_prompt = job_input.get("negative_prompt", " ")
        aspect_ratio = job_input.get("aspect_ratio", "16:9")
        width = job_input.get("width")
        height = job_input.get("height")
        num_inference_steps = job_input.get("num_inference_steps", 50)
        true_cfg_scale = job_input.get("true_cfg_scale", 4.0)
        seed = job_input.get("seed", 42)
        language = job_input.get("language", "en")
        
        # Magic prompts for better quality
        positive_magic = {
            "en": ", Ultra HD, 4K, cinematic composition.",
            "zh": ", 超清，4K，电影级构图."
        }
        
        # Aspect ratio configurations
        aspect_ratios = {
            "1:1": (1328, 1328),
            "16:9": (1664, 928),
            "9:16": (928, 1664),
            "4:3": (1472, 1140),
            "3:4": (1140, 1472),
            "3:2": (1584, 1056),
            "2:3": (1056, 1584),
        }
        
        # Get dimensions - prioritize custom width/height over aspect_ratio
        if width is not None and height is not None:
            # Use custom dimensions
            width = int(width)
            height = int(height)
        else:
            # Use aspect ratio
            width, height = aspect_ratios.get(aspect_ratio, aspect_ratios["16:9"])
        
        # Add magic prompt if language is supported
        final_prompt = prompt
        if language in positive_magic:
            final_prompt += positive_magic[language]
        
        # Generate image
        generator = torch.Generator(device=device).manual_seed(seed)
        
        image = pipe(
            prompt=final_prompt,
            negative_prompt=negative_prompt,
            width=width,
            height=height,
            num_inference_steps=num_inference_steps,
            true_cfg_scale=true_cfg_scale,
            generator=generator
        ).images[0]
        
        # Convert image to base64
        buffer = BytesIO()
        image.save(buffer, format="PNG")
        img_str = base64.b64encode(buffer.getvalue()).decode()
        
        return {
            "image": img_str,
            "width": width,
            "height": height,
            "prompt": final_prompt,
            "seed": seed
        }
        
    except Exception as e:
        return {"error": str(e)}

# Load model on startup
load_model()

# Start the serverless function
runpod.serverless.start({"handler": generate_image})