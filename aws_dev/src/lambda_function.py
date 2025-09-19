"""AWS Lambda function for caption generation using AWS Bedrock Claude 3.5 Sonnet."""
import json
import base64
import tempfile
import os
import mimetypes
from typing import Dict, Any
import boto3
from botocore.exceptions import BotoCoreError, ClientError

MODEL_ID = "us.anthropic.claude-3-5-sonnet-20241022-v2:0"


def generate_caption_lambda(
    image_b64: str,
    image_mime: str,
    video_description: str,
    aws_region: str = "us-east-2",
    max_tokens: int = 512,
    temperature: float = 1.0,
    show_log: bool = False,
) -> Dict[str, Any]:
    """Generate a caption from base64 image and video description - Lambda version."""
    try:
        # Fill prompt template
        filled_prompt = CAPTION_PROMPT.replace("{video_description}", video_description)
        
        if show_log:
            print(f"Image MIME: {image_mime}")
            print(f"Base64 length: {len(image_b64)}")
            print(f"Description: {video_description}")
        
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
                                "data": image_b64,
                            },
                        },
                        {"type": "text", "text": filled_prompt},
                    ],
                }
            ],
        }
        
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
    except Exception as e:
        return {"success": False, "error": f"Unexpected error: {str(e)}"}

def lambda_handler(event, context):
    """AWS Lambda handler function"""
    try:
        # Handle CORS preflight requests
        if event.get('httpMethod') == 'OPTIONS':
            return {
                'statusCode': 200,
                'headers': {
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Headers': 'Content-Type',
                    'Access-Control-Allow-Methods': 'POST, OPTIONS'
                },
                'body': ''
            }
        
        # Parse the incoming request
        body = json.loads(event.get('body', '{}'))
        
        # Extract image and description from the request
        image_data = body.get('image')  # base64 encoded image
        description = body.get('description', '')
        
        if not image_data or not description:
            return {
                'statusCode': 400,
                'headers': {
                    'Access-Control-Allow-Origin': '*',
                    'Content-Type': 'application/json'
                },
                'body': json.dumps({
                    'success': False,
                    'error': 'Missing image or description'
                })
            }
        
        # Detect MIME type from base64 header (if present) or default to JPEG
        image_mime = "image/jpeg"
        if image_data.startswith("data:"):
            # Remove data:image/jpeg;base64, prefix if present
            mime_part = image_data.split(';')[0].replace('data:', '')
            image_data = image_data.split(',')[1]
            image_mime = mime_part
        
        # Use your adapted function
        result = generate_caption_lambda(
            image_b64=image_data,
            image_mime=image_mime,
            video_description=description,
            show_log=True
        )
        
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Content-Type': 'application/json'
            },
            'body': json.dumps(result)
        }
        
    except Exception as e:
        print(f"Lambda error: {str(e)}")
        return {
            'statusCode': 500,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Content-Type': 'application/json'
            },
            'body': json.dumps({
                'success': False,
                'error': str(e)
            })
        }