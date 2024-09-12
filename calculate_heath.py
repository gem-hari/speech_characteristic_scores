import numpy as np
import parselmouth
from parselmouth.praat import call
import calculate_strength

def calculate_health(audio_path, f0min=75, f0max = 500, jitter_tolerance=0.02, jitter_multiplier=3000, shimmer_tolerance=0.11, shimmer_multiplier=1500,strength_score=None):
    result={}
    sound = parselmouth.Sound(audio_path)
    pointProcess = call(sound, "To PointProcess (periodic, cc)", f0min, f0max)
    localJitter = call(pointProcess, "Get jitter (local)", 0, 0, 0.0001, 0.02, 1.3)
    localShimmer =  call([sound, pointProcess], "Get shimmer (local)", 0, 0, 0.0001, 0.02, 1.3, 1.6)
    jitter_score = min(100,max(40,85 - (localJitter - jitter_tolerance)*jitter_multiplier))
    shimmer_score = min(100,max(40,85 - (localShimmer-shimmer_tolerance)*shimmer_multiplier))
    
    if strength_score is None:
        strength_score = calculate_strength.calculate_strength(audio_path)["strength_score"]
            
    health_score = 0.4*jitter_score+0.4*shimmer_score+0.2*strength_score
    result["health_score"] = health_score
    result["jitter_score"] = jitter_score
    result["shimmer_score"] = shimmer_score
    result["strength_score"] = strength_score
    return result
#print(calculate_health("year-olds.mp3"))
    
    