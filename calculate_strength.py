import numpy as np
import parselmouth
from parselmouth.praat import call

def get_rms(sound):
    rms = np.sqrt(np.mean(np.square(sound.values)))
    return rms

def get_intensity(sound):
    intensity = sound.to_intensity()
    mean_intensity = call(intensity, "Get mean", 0, 0, "dB")
    return mean_intensity

def get_harmonicity(sound):
    harmonicity = sound.to_harmonicity()
    mean_hnr = call(harmonicity, "Get mean", 0, 0)
    return mean_hnr

def normalize(value, min_val, max_val):
    return (value - min_val) / (max_val - min_val) * 100

def get_normalized_rms(rms,mean_rms,mean_rms_score):
    rms_score = (rms*mean_rms_score)/(mean_rms)
    return min(rms_score, 100)

def get_normalized_hnr(hnr,mean_hnr,mean_hnr_score):
    hnr_score = (hnr*mean_hnr_score)/(mean_hnr)
    return min(hnr_score,100)

def calculate_strength(audio_path,mean_rms=50, mean_rms_score=50,mean_hnr=5, mean_hnr_score=50):
    result = {}
    sound = parselmouth.Sound(audio_path)
    intensity = get_intensity(sound)
    rms = get_rms(sound)*1000
    hnr = get_harmonicity(sound)
    
    #print(" intensity is ", intensity)
    #print(" hnr is ", hnr)
    #print(" rms is ", rms)  

    normalized_intensity = min(100, intensity)
    normalized_rms = get_normalized_rms(rms,mean_rms,mean_rms_score)
    normalized_hnr = get_normalized_hnr(hnr,mean_hnr,mean_hnr_score)

    #print("normalised intensity is ", normalized_intensity)
    #print("normalised hnr is ", normalized_hnr)
    #print("normalised rms is ", normalized_rms)  
    
    strength_score = (0.4 * normalized_intensity + 0.3 * normalized_hnr + 0.3 * normalized_rms)
    strength_score = min(100, max(0, strength_score))
    
    result["intensity_score"] = normalized_intensity
    result["hnr_score"] = normalized_hnr
    result["rms_score"] = normalized_rms
    result["strength_score"] =strength_score
    #print(f"Strength score: {strength_score:.2f}")
    return result

#print(calculate_strength("full_confidence_1.mp3"))
    
    
 
    
    
    # Normalize the features

