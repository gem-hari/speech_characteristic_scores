import boto3
import json
import time
import amazon_transcribe
import calculate_stats_confidence_score_text
from botocore.exceptions import NoCredentialsError, PartialCredentialsError

def delete_from_s3(s3_client, bucket_name, object_key):
    try:
        s3_client.delete_object(Bucket=bucket_name, Key=object_key)
        print(f"Deleted {object_key} from bucket {bucket_name}")
        return True
    except NoCredentialsError:
        print("Credentials not available")
        return False
    except PartialCredentialsError:
        print("Incomplete credentials provided")
        return False
    except Exception as e:
        print(f"An error occurred while deleting from S3: {e}")
        return False

def calculate_score_confidence_transcribe(audio_name, delete_s3_result_json=True):
    bucket_name = 'interview-performance-analysis'
    audio_folder = 'audio'
    audio_file_name = audio_name
    REGION="ap-south-1"
    output_folder = "transcription_audio/"
    output_name = "transcription-"+audio_file_name[:-4]+"-"
    time_start = str(time.time())
    job_name = output_name + time_start

    transcribe_client = boto3.client(
        'transcribe',
        region_name=REGION
        )
    s3 = boto3.client(
            's3',
            region_name=REGION
    )

    transcript_file_uri = amazon_transcribe.amazon_transcribe_audio(transcribe_client,job_name,bucket_name,audio_folder,audio_file_name,output_folder,REGION="ap-south-1")
    response_key = output_folder+job_name+".json"
    response = s3.get_object(Bucket=bucket_name, Key=response_key)
    data_json = response['Body'].read().decode('utf-8')
    data_json = json.loads(data_json)
    
    if delete_s3_result_json:
        delete_from_s3(s3, bucket_name, response_key)
        
    result = calculate_stats_confidence_score_text.calculate_confidence_score(data_json)
    #print("Results for confidence are ", result)
    return result