"""
  Model configuration file 
"""

# Dictionary containing all available AI models
# Key = model identifier (what users select)
# Value = model configuration (how to use it)
MODELS = {
    "claude-sonnet-4": {
        "id":"us.anthropic.claude-3-5-sonnet-20241022-v2:0",

        # Provider name (tells us which handler class to use)
        "provider": "anthropic",

        # User-friendly information (for frontend dropdown)
        "name": "Claude Sonnet 4.0",
        "description": "Best for creative writing and complex reasoning",
        "icon": "🧠",

        # Technical specifications
        "supports_vision": True,
        "max_tokens_default": 512,
        "temperature_default": 0.7,

        # Usage limits (for production safety)
        "rate_limit_per_minute": 10,
        "daily_limit": 100,
        "enabled": True
      },

      "qwen-2.5-vl": {
          
        "id": "arn:aws:bedrock:us-east-2:324037274971:imported-model/v9ulmu1m3d1p",

        # Provider name (different from Anthropic)
        "provider": "qwen",

        # User-friendly information
        "name": "QWen 2.5 VL",
        "description": "Fast and efficient vision-language model",
        "icon": "⚡",

        # Technical specifications
        "supports_vision": True,
        "max_tokens_default": 512,
        "temperature_default": 0.7,

        # Usage limits (QWen might be cheaper, so higher limits)
        "rate_limit_per_minute": 30,
        "daily_limit": 500,
        "enabled": True
      }
  }
"""
Get configuration for a specific model.
      
Args:
    model_key: The model identifier (e.g.,'claude-sonnet-4')
          
    Returns:
        dict: Model configuration
          
    Raises:
        ValueError: If model doesn't exist
          
    Why this function exists:
    - Provides error checking (what if user passes invalid model?)
    - Single place to handle model lookup logic
    - Can add logging/monitoring here later
 """
def get_model_config(model_key: str) -> dict:
 
      if model_key not in MODELS:
          available_models = list(MODELS.keys())
          raise ValueError(f"Unknown model '{model_key}'. Available models: {available_models}")

      config = MODELS[model_key]

      # Check if model is enabled
      if not config.get("enabled", True):
        raise ValueError(f"Model '{model_key}' is currently disabled")

      return config

"""
Get list of all available and enabled models.
      
Returns:
    list: List of model configurations for frontend
          
Why this function exists:
    - Frontend needs to populate dropdown options
    - Only returns enabled models
    - Returns user-friendly information (name, description, icon)
 """
def get_available_models() -> list:
      
    available = []

    for model_key, config in MODELS.items():
        # Only include enabled models
        if config.get("enabled", True):
              available.append({
                  "id": model_key,
                  "name": config["name"],
                  "description": config["description"],
                  "icon": config.get("icon", "🤖"),
                  "provider": config["provider"]
              })

    return available