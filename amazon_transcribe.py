import boto3
import json
from pprint import pprint
import time


def start_transcription_job(transcribe_client, job_name,job_uri, media_format,language_code, bucket_name,output_key):
    response = transcribe_client.start_transcription_job(
        TranscriptionJobName=job_name,
        Media={'MediaFileUri': job_uri},
        MediaFormat=media_format,
        LanguageCode = language_code,
        OutputBucketName=bucket_name,
        OutputKey=output_key
    )
    return response


def check_transcription_job_status(transcribe_client, job_name):
    while True:
        response = transcribe_client.get_transcription_job(TranscriptionJobName=job_name)
        status = response['TranscriptionJob']['TranscriptionJobStatus']
        print(f'Job status: {status}')
        if status in ['COMPLETED', 'FAILED']:
            return response
        time.sleep(5)

def amazon_transcribe_audio(transcribe_client,job_name,bucket_name,audio_folder,audio_file_name,output_key,REGION="ap-south-1"):    
    job_uri = f's3://{bucket_name}/{audio_folder}/{audio_file_name}'
    language_code = 'en-US'
    media_format = audio_file_name.split(".")[-1]
    
    response = start_transcription_job(transcribe_client,job_name,job_uri, media_format,language_code, bucket_name, output_key)
    result = check_transcription_job_status(transcribe_client, job_name)
    transcript_file_uri = result['TranscriptionJob']['Transcript']['TranscriptFileUri']
    
    return transcript_file_uri
    
"""
bucket_name = 'interview-performance-analysis'
audio_folder = 'audio'
audio_file_name = 'hindi-english.wav'
REGION="ap-south-1"
output_folder = "transcription_audio/"
output_name = "transcription-"+audio_file_name[:-4]+"-"
time_start = str(time.time())
job_name = output_name + time_start

transcribe_client = boto3.client(
    'transcribe',
    region_name=REGION
    )



transcript_file_uri = amazon_transcribe_audio(transcribe_client,job_name,bucket_name,audio_folder,audio_file_name,output_folder,REGION="ap-south-1")"""