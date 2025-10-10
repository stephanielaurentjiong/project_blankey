"""
  Base handler class that defines the interface all AI model handlers must follow.
  This is an example of 'Abstract Base Class' - a blueprint for other classes.
"""

"""
Abstract base class for all AI model handlers.
      
Why we need this:
- Ensures all handlers have the same methods (consistency)
- Makes it easy to add new models (they just follow this pattern)
- Helps catch errors early (if someone forgets a method)
"""
class BaseModelHandler:
    
    """
     Build the API request payload for this specific model.
          
    Args:
    image_b64: Base64 encoded image data
    image_mime: Image MIME type (e.g., 'image/jpeg')
    prompt: The text prompt to send to the model
    max_tokens: Maximum tokens in response
    temperature: Creativity level (0.0 = focused, 1.0 = creative)
              
    Returns:
    dict: The payload to send to the AI model's API
              
    Why this method exists:
    - Each AI model expects different payload formats
    - Claude wants "messages" array, QWen wants "prompt" string
 - This method handles those differences
    """
    def build_payload(self, image_b64: str, image_mime: str, prompt: str, max_tokens: int, temperature: float) -> dict:
          
        raise NotImplementedError("Each handler must implement build_payload method")

    """
    Extract the generated text from the AI model's response.
          
    Args: 
    response_json: The raw JSON response from the AI model
              
    Returns:
    str: The generated caption text
              
    Why this method exists:
    - Each AI model returns responses in different formats
    - Claude: response['content'][0]['text']
    - QWen: response['choices'][0]['text']
    - This method handles those differences
    """
    def parse_response(self, response_json: dict) -> str:
         
        raise NotImplementedError("Each handler must implement parse_response method")

    """
    Return information about this model .
          
    Returns:
    dict: Model metadata like name, description, etc.
              
    Why this is useful:
    - Can return model-specific info for debugging
    - Helpful for logging which model was used
    - Can be extended for model-specific features
    """
    def get_model_info(self) -> dict:
          
        return {
            "handler_type": self.__class__.__name__,
            "description": "Base handler class"
        }