"""Main caption generation function using AWS Bedrock Claude 3.5 Sonnet."""

import json
from typing import Dict, Any
import boto3
from botocore.exceptions import BotoCoreError, ClientError

from utils import load_prompt_template, resolve_image_path, encode_image_to_base64, detect_mime_type

MODEL_ID = "us.anthropic.claude-3-5-sonnet-20241022-v2:0"


def generate_caption(
    image_path: str,
    video_description: str,
    prompt_file: str = "phase0/prompts/caption_generation_prompt.txt",
    aws_region: str = "us-east-2",
    max_tokens: int = 512,
    temperature: float = 1.0,
    show_log: bool = False,
) -> Dict[str, Any]:
    """Generate a caption from an image and video description."""
    try:
        # Load prompt
        prompt_template = load_prompt_template(prompt_file)
        filled_prompt = prompt_template.replace("{video_description}", video_description)

        # Resolve image and encode
        resolved_image_path = resolve_image_path(image_path)
        image_b64 = encode_image_to_base64(resolved_image_path)
        image_mime = detect_mime_type(resolved_image_path)

        if show_log:
            print(f"Image path: {resolved_image_path}")
            print(f"Image MIME: {image_mime}")
            print(f"Base64 length: {len(image_b64)}")
            print(f"Base64 starts with: {image_b64[:50]}...")

        # Build payload
        payload = {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": max_tokens,
            "temperature": temperature,
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image",
                            "source": {
                                "type": "base64",
                                "media_type": image_mime,
                                "data": image_b64,  # raw base64 string ONLY
                            },
                        },
                        {"type": "text", "text": filled_prompt},
                    ],
                }
            ],
        }

        if show_log:
            print(f"Payload: {json.dumps(payload, indent=2)[:800]}")
            # Add preview log
            preview_len = 100
            print(f"Encoded image (first {preview_len} chars): {image_b64[:preview_len]}")
            print(f"Total base64 length: {len(image_b64)}")

        # Invoke model
        bedrock = boto3.client("bedrock-runtime", region_name=aws_region)
        response = bedrock.invoke_model(modelId=MODEL_ID, body=json.dumps(payload))

        # Parse response
        raw = response.get("body")
        text = raw.read().decode("utf-8") if hasattr(raw, "read") else str(raw)
        response_json = json.loads(text)
        output_text = response_json['content'][0]['text']

        return {"success": True, "output_text": output_text}

    except (BotoCoreError, ClientError) as e:
        return {"success": False, "error": f"AWS error: {str(e)}"}
    except FileNotFoundError as e:
        return {"success": False, "error": f"File error: {str(e)}"}
    except Exception as e:
        return {"success": False, "error": f"Unexpected error: {str(e)}"}
