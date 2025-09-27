"""AWS Lambda function for caption generation using AWS Bedrock Claude 3.5 Sonnet."""
import json
import base64
import tempfile
import os
import mimetypes
from typing import Dict, Any
import boto3
from botocore.exceptions import BotoCoreError, ClientError
from utils.caption_util import load_prompt_template
import io


MODEL_ID = "us.anthropic.claude-3-5-sonnet-20241022-v2:0"


def parse_multipart_form_data(body: bytes, content_type: str) -> Dict[str, Any]:
    """Parse multipart form data from Lambda event."""
    try:
        # Extract boundary from content type
        boundary = content_type.split('boundary=')[1].encode('utf-8')
        
        # Split the body by boundary
        parts = body.split(b'--' + boundary)
        
        result = {}
        
        for part in parts:
            if b'Content-Disposition: form-data' not in part:
                continue
                
            # Extract field name
            if b'name="image"' in part:
                # This is the image field
                header_end = part.find(b'\r\n\r\n')
                if header_end != -1:
                    image_data = part[header_end + 4:]
                    # Remove trailing boundary markers
                    if image_data.endswith(b'\r\n'):
                        image_data = image_data[:-2]
                    
                    result['image_data'] = image_data
                    result['image_filename'] = 'uploaded_image.jpg'
                    result['image_content_type'] = 'image/jpeg'
                    
            elif b'name="description"' in part:
                # This is the description field
                header_end = part.find(b'\r\n\r\n')
                if header_end != -1:
                    description = part[header_end + 4:]
                    # Remove trailing boundary markers
                    if description.endswith(b'\r\n'):
                        description = description[:-2]
                    
                    result['description'] = description.decode('utf-8')
        
        return result
        
    except Exception as e:
        print(f"Error parsing multipart data: {str(e)}")
        return {}


def convert_image_to_base64(image_data: bytes, mime_type: str) -> str:
    """Convert image bytes to base64 string."""
    return base64.b64encode(image_data).decode('utf-8')


def generate_caption_lambda(
    image_b64: str,
    image_mime: str,
    video_description: str,
    prompt_file: str = 'prompt.txt',
    aws_region: str = "us-east-2",
    max_tokens: int = 512,
    temperature: float = 1.0,
    show_log: bool = False,
) -> Dict[str, Any]:
    """Generate a caption from base64 image and video description - Lambda version."""
    try:
        # Fill prompt template
        prompt_template = load_prompt_template(prompt_file)
        filled_prompt = prompt_template.replace("{video_description}", video_description)
        
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
        
        # Get content type and body
        content_type = event.get('headers', {}).get('content-type', '')
        body = event.get('body', '')
        
        # Handle base64 encoded body (API Gateway encodes binary data)
        if event.get('isBase64Encoded', False):
            body_bytes = base64.b64decode(body)
        else:
            body_bytes = body.encode('utf-8') if isinstance(body, str) else body
        
        # Check if it's multipart form data
        if 'multipart/form-data' in content_type:
            # Parse multipart form data
            form_data = parse_multipart_form_data(body_bytes, content_type)
            
            if not form_data.get('image_data') or not form_data.get('description'):
                return {
                    'statusCode': 400,
                    'headers': {
                        'Access-Control-Allow-Origin': '*',
                        'Content-Type': 'application/json'
                    },
                    'body': json.dumps({
                        'success': False,
                        'error': 'Missing image or description in form data'
                    })
                }
            
            # Convert image to base64
            image_b64 = convert_image_to_base64(
                form_data['image_data'], 
                form_data['image_content_type']
            )
            image_mime = form_data['image_content_type']
            description = form_data['description']
            
            print(f"Received file: {form_data.get('image_filename', 'unknown')}")
            print(f"File size: {len(form_data['image_data'])} bytes")
            print(f"MIME type: {image_mime}")
            
        else:
            # Fallback to JSON parsing for backward compatibility
            try:
                body_str = body_bytes.decode('utf-8') if isinstance(body_bytes, bytes) else str(body_bytes)
                body_json = json.loads(body_str)
                image_data = body_json.get('image')
                description = body_json.get('description', '')
                
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
                
                image_b64 = image_data
                
            except json.JSONDecodeError:
                return {
                    'statusCode': 400,
                    'headers': {
                        'Access-Control-Allow-Origin': '*',
                        'Content-Type': 'application/json'
                    },
                    'body': json.dumps({
                        'success': False,
                        'error': 'Invalid request format'
                    })
                }
        
        # Use your adapted function
        result = generate_caption_lambda(
            image_b64=image_b64,
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