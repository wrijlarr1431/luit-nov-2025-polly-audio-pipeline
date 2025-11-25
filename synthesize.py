#!/usr/bin/env python3
"""
Amazon Polly Text-to-Speech Synthesizer
Converts text files to MP3 audio using AWS Polly
"""

import os
import sys
import boto3
from pathlib import Path

def validate_environment():
    """
    Validate required environment variables are set
    
    Returns:
        tuple: (bucket_name, aws_region)
    """
    bucket_name = os.environ.get('S3_BUCKET_NAME')
    aws_region = os.environ.get('AWS_REGION', 'us-east-1')
    
    if not bucket_name:
        print("❌ ERROR: S3_BUCKET_NAME environment variable not set")
        print("   Set it with: export S3_BUCKET_NAME='your-bucket-name'")
        sys.exit(1)
    
    return bucket_name, aws_region

def read_text_file(filepath):
    """
    Read text content from file
    
    Args:
        filepath (str): Path to text file
    
    Returns:
        str: Text content
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            text = file.read().strip()
        
        if not text:
            print(f"❌ ERROR: File {filepath} is empty")
            sys.exit(1)
        
        print(f"✅ Read {len(text)} characters from {filepath}")
        return text
    
    except FileNotFoundError:
        print(f"❌ ERROR: File {filepath} not found")
        sys.exit(1)
    except Exception as e:
        print(f"❌ ERROR reading file: {e}")
        sys.exit(1)

def synthesize_speech(text, output_file, aws_region):
    """
    Convert text to speech using Amazon Polly
    
    Args:
        text (str): Text to convert
        output_file (str): Path to save MP3 file
        aws_region (str): AWS region
    
    Returns:
        bool: True if successful
    """
    try:
        # Initialize Polly client
        polly_client = boto3.client('polly', region_name=aws_region)
        
        print(f"  Synthesizing speech with Amazon Polly...")
        print(f"   Voice: Joanna (Neural)")
        print(f"   Engine: Neural")
        print(f"   Text length: {len(text)} characters")
        
        # Call Polly API
        response = polly_client.synthesize_speech(
            Text=text,
            OutputFormat='mp3',
            VoiceId='Joanna',
            Engine='neural'
        )
        
        # Save audio stream to file
        if 'AudioStream' in response:
            with open(output_file, 'wb') as file:
                file.write(response['AudioStream'].read())
            
            file_size = os.path.getsize(output_file)
            print(f" Audio synthesized successfully!")
            print(f"   Output: {output_file}")
            print(f"   Size: {file_size:,} bytes")
            return True
        else:
            print(" ERROR: No audio stream in Polly response")
            return False
    
    except Exception as e:
        print(f" ERROR during synthesis: {e}")
        return False

def upload_to_s3(local_file, bucket_name, s3_key, aws_region):
    """
    Upload file to S3 bucket
    
    Args:
        local_file (str): Path to local file
        bucket_name (str): S3 bucket name
        s3_key (str): S3 object key (path in bucket)
        aws_region (str): AWS region
    
    Returns:
        bool: True if successful
    """
    try:
        s3_client = boto3.client('s3', region_name=aws_region)
        
        print(f"  Uploading to S3...")
        print(f"   Bucket: {bucket_name}")
        print(f"   Key: {s3_key}")
        
        s3_client.upload_file(
            local_file,
            bucket_name,
            s3_key,
            ExtraArgs={
                'ContentType': 'audio/mpeg',
                'Metadata': {
                    'source': 'polly-pipeline',
                    'voice': 'Joanna',
                    'engine': 'neural'
                }
            }
        )
        
        print(f" Upload successful!")
        print(f"   S3 URL: s3://{bucket_name}/{s3_key}")
        return True
    
    except Exception as e:
        print(f" ERROR during upload: {e}")
        return False

def main():
    """Main execution function"""
    
    print("\n" + "="*60)
    print("  AMAZON POLLY TEXT-TO-SPEECH SYNTHESIZER")
    print("="*60 + "\n")
    
    # Step 1: Validate environment
    bucket_name, aws_region = validate_environment()
    
    # Step 2: Configuration
    input_file = 'speech.txt'
    output_file = 'output.mp3'
    
    # Get environment-specific S3 key
    environment = os.environ.get('ENVIRONMENT', 'dev')
    if environment == 'beta':
        s3_key = 'polly-audio/beta.mp3'
    elif environment == 'prod':
        s3_key = 'polly-audio/prod.mp3'
    else:
        s3_key = 'polly-audio/dev.mp3'
    
    print(f" Configuration:")
    print(f"   Input file: {input_file}")
    print(f"   Output file: {output_file}")
    print(f"   S3 bucket: {bucket_name}")
    print(f"   S3 key: {s3_key}")
    print(f"   AWS region: {aws_region}")
    print(f"   Environment: {environment}")
    print()
    
    # Step 3: Read input text
    text = read_text_file(input_file)
    
    # Step 4: Synthesize speech
    success = synthesize_speech(text, output_file, aws_region)
    if not success:
        sys.exit(1)
    
    # Step 5: Upload to S3
    success = upload_to_s3(output_file, bucket_name, s3_key, aws_region)
    if not success:
        sys.exit(1)
    
    # Step 6: Cleanup local file (optional)
    if os.path.exists(output_file):
        os.remove(output_file)
        print(f"🗑️  Cleaned up local file: {output_file}")
    
    print("\n" + "="*60)
    print(" PIPELINE COMPLETE!")
    print("="*60 + "\n")
    
    sys.exit(0)

if __name__ == '__main__':
    main()