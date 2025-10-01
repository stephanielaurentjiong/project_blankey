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
import uuid
from datetime import datetime

#MODEL_ID = "us.anthropic.claude-3-5-sonnet-20241022-v2:0" # Claude Sonnet 3.5
MODEL_ID = 'arn:aws:bedrock:us-east-2:324037274971:imported-model/v9ulmu1m3d1p' # Qwen 2.5 VL Instruct 3B Pretrained


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
                # Extract MIME type from Content-Type header
                content_type_line = None
                for line in part.split(b'\r\n'):
                    if line.startswith(b'Content-Type:'):
                        content_type_line = line.decode('utf-8')
                        break
                
                # Extract filename from Content-Disposition header
                filename = None
                for line in part.split(b'\r\n'):
                    if b'filename=' in line:
                        filename_start = line.find(b'filename="') + 10
                        filename_end = line.find(b'"', filename_start)
                        if filename_start > 9 and filename_end > filename_start:
                            filename = line[filename_start:filename_end].decode('utf-8')
                        break
                
                # Get image data
                header_end = part.find(b'\r\n\r\n')
                if header_end != -1:
                    image_data = part[header_end + 4:]
                    # Remove trailing boundary markers
                    if image_data.endswith(b'\r\n'):
                        image_data = image_data[:-2]
                    
                    result['image_data'] = image_data
                    result['image_filename'] = filename or 'uploaded_image'
                    
                    # Extract MIME type from Content-Type header
                    if content_type_line:
                        mime_type = content_type_line.split(': ')[1].strip()
                        result['image_content_type'] = mime_type
                    else:
                        result['image_content_type'] = 'image/jpeg'  # fallback
                    
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


def get_extension_from_mime(mime_type: str) -> str:
    """Get file extension from MIME type."""
    if not mime_type:
        return '.jpg'  # fallback
    
    # Map MIME types to extensions
    mime_to_ext = {
        'image/jpeg': '.jpg',
        'image/jpg': '.jpg', 
        'image/png': '.png',
        'image/gif': '.gif',
        'image/webp': '.webp',
        'image/bmp': '.bmp',
        'image/tiff': '.tiff',
        'image/svg+xml': '.svg',
        'image/heic': '.heic',
        'image/heif': '.heif'
    }
    
    return mime_to_ext.get(mime_type.lower(), '.jpg')


def is_supported_format(mime_type: str) -> bool:
    """Check if image format is supported by Bedrock Claude."""
    supported_formats = {
        'image/jpeg',
        'image/jpg', 
        'image/png',
        'image/gif',
        'image/webp'
    }
    return mime_type.lower() in supported_formats


def convert_unsupported_format(mime_type: str) -> str:
    """Convert unsupported format to JPEG for Bedrock compatibility."""
    unsupported_to_jpeg = {
        'image/heic': 'image/jpeg',
        'image/heif': 'image/jpeg',
        'image/bmp': 'image/jpeg',
        'image/tiff': 'image/jpeg',
        'image/svg+xml': 'image/jpeg'
    }
    return unsupported_to_jpeg.get(mime_type.lower(), mime_type)  # Return original if not in conversion map


def generate_caption_lambda(
    image_b64: str,
    image_mime: str,
    video_description: str,
    prompt_file: str = 'prompt.txt',
    aws_region: str = "us-east-2",
    max_tokens: int = 512,
    temperature: float = 0.7,
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

        '''       
        # Claude payload
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
        '''   
        # Qwen 2.5 VL Payload
        # Format: <|vision_start|><|image_pad|><|vision_end|> followed by the text prompt
        payload = {
            "prompt": f"<|vision_start|><|image_pad|><|vision_end|>\n\n{filled_prompt}",
            "images": [image_b64],
            "max_new_tokens": max_tokens,
            "temperature": temperature
        }

        # Invoke model
        bedrock = boto3.client("bedrock-runtime", region_name=aws_region)
        response = bedrock.invoke_model(modelId=MODEL_ID, body=json.dumps(payload))
        
        # Parse response
        raw = response.get("body")
        text = raw.read().decode("utf-8") if hasattr(raw, "read") else str(raw)
        response_json = json.loads(text)
        #output_text = response_json['content'][0]['text'] # Claude Output Format
        output_text = response_json['choices'][0]['text'] # Qwen 2.5 VL Output Format
        
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
            original_mime = form_data['image_content_type']
            description = form_data['description']
            
            print(f"Received file: {form_data.get('image_filename', 'unknown')}")
            print(f"File size: {len(form_data['image_data'])} bytes")
            print(f"Original MIME type: {original_mime}")
            
            # Check if format is supported by Bedrock
            if not is_supported_format(original_mime):
                print(f"⚠️  Unsupported format: {original_mime}")
                print(f"   Converting to JPEG for Bedrock compatibility")
                image_mime = convert_unsupported_format(original_mime)
            else:
                image_mime = original_mime
                print(f"✅ Supported format: {image_mime}")
            
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
        
        # Use adapted function with timing
        start_time = datetime.now()
        result = generate_caption_lambda(
            image_b64=image_b64,
            image_mime=image_mime,
            video_description=description,
            show_log=True
        )
        end_time = datetime.now()
        generation_time_ms = int((end_time - start_time).total_seconds() * 1000)
        
        # Store data to S3
        if result['success']:
            try:
                s3_client = boto3.client('s3')
                bucket_name = 'project-blankey'

                date_str = datetime.now().strftime('%Y-%m-%d')
                request_id = str(uuid.uuid4())
                
                # Get proper file extension from MIME type
                file_extension = get_extension_from_mime(image_mime)
                image_key = f'chat_data/{date_str}/images/{request_id}{file_extension}'
                data_key = f'chat_data/{date_str}/{date_str}.json'

                # Upload image file
                s3_client.put_object(
                    Bucket=bucket_name,
                    Key=image_key,
                    Body=form_data['image_data'] if 'form_data' in locals() else base64.b64decode(image_b64),
                    ContentType=image_mime
                )

                # Load existing data for the day, or create new
                try:
                    existing_data = s3_client.get_object(Bucket=bucket_name, Key=data_key)
                    daily_log = json.loads(existing_data['Body'].read().decode('utf-8'))
                except s3_client.exceptions.NoSuchKey:
                    # First interaction of the day
                    daily_log = {
                        'date': date_str,
                        'interactions': []
                    }

                # Add new interaction directly
                daily_log['interactions'].append({
                    'request_id': request_id,
                    'timestamp': datetime.now().isoformat(),
                    'image_key': image_key,
                    'description': description,
                    'output': result['output_text'],
                    'model_used': MODEL_ID,
                    'generation_time_ms': generation_time_ms
                })

                # Upload updated daily log
                s3_client.put_object(
                    Bucket=bucket_name,
                    Key=data_key,
                    Body=json.dumps(daily_log, indent=2, ensure_ascii=False),
                    ContentType='application/json'
                )
                
                print(f"✅ Stored to S3:")
                print(f"   Image: s3://{bucket_name}/{image_key}")
                print(f"   Data: s3://{bucket_name}/{data_key}")
                print(f"   Total interactions today: {len(daily_log['interactions'])}")
                print(f"   Generation time: {generation_time_ms}ms")
                
            except Exception as s3_error:
                print(f"⚠️  S3 storage failed: {str(s3_error)}")
                # Continue without failing the request
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