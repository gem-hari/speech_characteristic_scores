driver.py is the entry point
Name of the file should be mentioned in audio_name in driver.py
Gender should be mentioned for deepness score calculation
Acoustic model is downloaded from https://github.com/amritkromana/disfluency_detection_from_audio
Everything was done using python==3.10.11

steps to download the model
mkdir demo_models && cd demo_models
gdown --id 1wWrmopvvdhlBw-cL7EDyih9zn_IJu5Wr -O acoustic.pt

#calculate_confidence_score_acoustic.py has the files related to acoustic model
#calculate_score_transcribe uses amazon transcribe and stats based on that
#for using transcribe file has to be uploaded to s3 bucket 
#for using acoustic file has to be in same folder as driver.py
