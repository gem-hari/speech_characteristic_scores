import json
import re
import numpy as np
import requests

def speech_speed_segment(wpm_rate):
    if 70 < wpm_rate <= 150:
        speed = 'Medium'
        speed_score = 10
    elif 150 < wpm_rate <= 200:
        speed = 'Medium to Fast'
        speed_score = 8
    elif wpm_rate <= 70:
        speed = 'Slow'
        speed_score = 5
    else:
        speed = 'Fast'
        speed_score = 5
    return speed, speed_score

def calculate_consistency_score(speech_rates):
    values = np.array(speech_rates)
    min_val = np.min(values)
    max_val = np.max(values)
    mean_rate = np.mean(values)
    std_dev = 0
    if min_val == max_val:
        return 10, mean_rate, std_dev
    min_max_scaled = (values - min_val) / (max_val - min_val)
    std_dev = np.std(min_max_scaled)
    consistency_score = 10 * (1 - std_dev)
    return consistency_score, mean_rate, std_dev

def find_filler_words(text):
    speech_text = ''
    
    speech_text = re.split(r'[ ,.]', text)
    filler_words = ["like","Uh","uh" ,"um", "Um", "Um...", "Um..", "might", "aa", "aaa", "mean", "know", "well", "Well", "Oh", "oh",
                "really", "basically", "oh", "maybe", "somehow", "Hi..", "Hi...", "Well", "like", "know", "mean"]

    total_filler_words = 0
    for word in filler_words:
        total_filler_words += speech_text.count(word)
    percent = (total_filler_words / max(len(speech_text), 1)) * 100
    score = 0
    if percent <= 5:
      score = 10
    elif percent <= 10:
      score = 8
    elif percent <= 20:
      score = 6
    elif percent <= 30:
      score = 4
    else:
      score = 2
    return total_filler_words, percent, score

def calculate_pause_score(total_pause_sec,  segment_len_sec):
  pause_to_speech_ratio = total_pause_sec/np.sum(segment_len_sec)
  if pause_to_speech_ratio <= 0.3:
    pause_score = 10
  elif pause_to_speech_ratio >= 1.2:
    pause_score = 6
  else:
    pause_score = 8
  return pause_score

def preprocess_audio(aws_transcript):
  data = {}
  segment_wpm_list = []
  data["transcript"] = aws_transcript['results']['transcripts']
  data["audio_segments"] = aws_transcript['results']['audio_segments']
  
  for segment in data['audio_segments']:
    transcript = segment['transcript']
    segment_wpm = len(segment['items'])/((float(segment['end_time'])- float(segment['start_time']))/60)
    segment_wpm_list.append(segment_wpm)
    segment_speed,segment_speed_score = speech_speed_segment(segment_wpm)
    total_filler_words, percent, segment_filler_score = find_filler_words(transcript)
    segment['segment_wpm'] = segment_wpm
    segment['segment_speed_score'] = segment_speed_score
    segment['segment_filler_score'] = segment_filler_score
  return data, segment_wpm_list

def calculate_confidence_score(data):
  result = {}
  data, segment_wpm_list = preprocess_audio(data)
  segment_speed_score = []
  segment_filler_score = []
  segment_len_sec = []
  total_pause_sec = 0
  last_segment_end_time = -1

  for segment in data['audio_segments']:
    segment_speed_score.append(segment['segment_speed_score'])
    segment_filler_score.append(segment['segment_filler_score'])
    segment_len_sec.append(float(segment['end_time'])- float(segment['start_time']))
    if last_segment_end_time == -1:
      last_segment_end_time = float(segment['end_time'])
    else:
      total_pause_sec += float(segment['start_time']) - last_segment_end_time
  data["mean_speed_score"] = np.mean(segment_speed_score)
  data["mean_filler_score"] = np.mean(segment_filler_score)
  data["consistency_score"],  mean_rate, std_dev= calculate_consistency_score(segment_speed_score)
  data["calculate_pause_score"] = calculate_pause_score(total_pause_sec, segment_len_sec)
  
  result["mean_speed_score"] = data["mean_speed_score"]*10
  result["mean_filler_score"] = data["mean_filler_score"]*10
  #result["consistency_score"] = data["consistency_score"]*10
  #consistency is more suited for monotonicity
  result["calculate_pause_score"] = data["calculate_pause_score"]*10 
  result["segment_wpm_list"] = segment_wpm_list
  return result

#import json
#aws_transcript_path = "transcription_stutteringsample.json"
#with open(aws_transcript_path, 'r') as file:
#    aws_transcript = json.load(file)
#print(calculate_confidence_score(aws_transcript))

