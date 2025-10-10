"""
QWen 2.5 VL model handler.
This class knows how to communicate with QWen models through AWS Bedrock.
"""

from .base_handler import BaseModelHandler

class QwenHandler(BaseModelHandler):
    """
    Handler for QWen 2.5 VL (Vision-Language) model.
    
    QWen models use a different API format than Claude:
    - Simple prompt string format (not messages array)
    - Special vision tokens (<|vision_start|>, <|image_pad|>, <|vision_end|>)
    - Different field names (max_new_tokens instead of max_tokens)
    - Different response structure
    """
    
    def build_payload(self, image_b64: str, image_mime: str, prompt: str, max_tokens: int, temperature: float) -> dict:
        """
        Build the API payload that QWen expects.
        
        Args:
            image_b64: Base64 encoded image
            image_mime: Image type (not used by QWen, but kept for consistency)
            prompt: Text prompt for the AI
            max_tokens: Maximum response length
            temperature: Creativity level (0.0-1.0)
            
        Returns:
            dict: Payload formatted for QWen API
            
        QWen's Expected Format:
        {
            "prompt": "<|vision_start|><|image_pad|><|vision_end|>\n\nYour prompt here",
            "images": ["base64_image_data"],
            "max_new_tokens": 512,
            "temperature": 0.7
        }
        
        Key Differences from Claude:
        - Uses "prompt" string instead of "messages" array
        - Requires special vision tokens around image
        - Uses "max_new_tokens" instead of "max_tokens"
        - Images passed as separate array
        """
        # QWen requires these special tokens to understand where the image goes
        vision_prompt = f"<|vision_start|><|image_pad|><|vision_end|>\n\n{prompt}"
        
        payload = {
            # QWen's prompt format with vision tokens
            "prompt": vision_prompt,
            
            # Images passed as array of base64 strings
            "images": [image_b64],
            
            # QWen uses "max_new_tokens" (tokens to generate)
            # vs Claude's "max_tokens" (total tokens including input)
            "max_new_tokens": max_tokens,
            
            # Temperature works the same way
            "temperature": temperature
        }
        
        return payload
    
    def parse_response(self, response_json: dict) -> str:
        """
        Extract the generated text from QWen's response.
        
        Args:
            response_json: Raw response from QWen API
            
        Returns:
            str: The generated caption text
            
        QWen's Response Format:
        {
            "choices": [
                {
                    "text": "The actual generated caption here",
                    "finish_reason": "stop"
                }
            ],
            "usage": {...}
        }
        
        Key Differences from Claude:
        - Uses "choices" array instead of "content" array
        - Text is directly in choices[0]["text"]
        - No nested structure like Claude's content blocks
        """
        try:
            # Navigate through QWen's response structure
            # response_json['choices'] = array of generated choices
            # [0] = first (and usually only) choice
            # ['text'] = the actual generated text
            generated_text = response_json['choices'][0]['text']
            
            return generated_text
            
        except (KeyError, IndexError) as e:
            # If response structure is unexpected, provide helpful error
            raise ValueError(f"Unexpected QWen response format: {e}. Response: {response_json}")
    
    def get_model_info(self) -> dict:
        """
        Return information about this handler.
        
        Returns:
            dict: Handler metadata
        """
        return {
            "handler_type": "QwenHandler",
            "description": "Handler for QWen 2.5 VL model via AWS Bedrock",
            "vision_tokens_required": True,
            "supports_multiple_images": True,
            "max_images_per_request": 1  # Current limitation
        }