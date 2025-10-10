"""
Anthropic Claude model handler.
This class knows how to communicate with Claude models through AWS Bedrock.
"""

from .base_handler import BaseModelHandler

"""
Handler for Anthropic Claude models (Claude 3.5 Sonnet, etc.)
"""
class AnthropicHandler(BaseModelHandler):
      
    """
    Build the API payload that Claude expects.
          
    Args:
        image_b64: Base64 encoded image
        image_mime: Image type (e.g., 'image/jpeg')
        prompt: Text prompt for the AI
        max_tokens: Maximum response length
        temperature: Creativity level (0.0-1.0)
              
    Returns:
        dict: Payload formatted for Claude API
    """
    def build_payload(self, image_b64: str, image_mime: str, prompt: str, max_tokens: int, temperature: float) -> dict:
          
        payload = {
            # Claude requires this specific version string
            "anthropic_version": "bedrock-2023-05-31",

            # Token and temperature settings
            "max_tokens": max_tokens,
            "temperature": temperature,

            # Messages array (Claude's conversation format)
            "messages": [
                {
                    "role": "user",  # Always "user" for single requests
                    "content": [
                        {
                            # Image content block
                            "type": "image",
                            "source": {
                                "type": "base64",
                                "media_type": image_mime,  # Important: must match actual image type
                                "data": image_b64,
                            },
                        },
                        {   
                        # Text content block  
                        "type": "text",
                        "text": prompt
                        },
                    ],
                }
            ],
        }

        return payload

    """
    Extract the generated text from Claude's response.
          
    Args:
        response_json: Raw response from Claude API
              
    Returns:
        str: The generated caption text
    """
    def parse_response(self, response_json: dict) -> str:
          
        try:
            generated_text = response_json['content'][0]['text']
            return generated_text

        except (KeyError, IndexError) as e:
            # If response structure is unexpected, provide error
            raise ValueError(f"Unexpected Claude response format: {e}. Response: {response_json}")

    def get_model_info(self) -> dict:
        return {
            "handler_type": "AnthropicHandler",
            "description": "Handler for Anthropic Claude models via AWS Bedrock",
            "api_version": "bedrock-2023-05-31",
            "supported_models": ["claude-3-5-sonnet", "claude-3-haiku", "claude-3-opus"]}
