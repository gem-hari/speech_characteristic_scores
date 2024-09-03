import parselmouth
import librosa
import numpy as np
from parselmouth.praat import call
def calculate_monotonicity_score(audio_path, sentence_wpm, max_std_wpm=50):
    result ={}
    sound = parselmouth.Sound(audio_path)
    amplitudes = sound.values
    pitch = call(sound, "To Pitch", 0.0, 75, 500)
    frequencies = pitch.selected_array['frequency']
    frequencies = frequencies[frequencies>0]  

    #pitch variation
    pitch_variation = 100 -(np.std(frequencies)/np.mean(frequencies))*100
    #print("Pitch variation is ", pitch_variation)

    #energy variation
    rms = librosa.feature.rms(y=amplitudes)[0]
    rms = rms[rms>0]
    rms = (rms - np.min(rms))/(np.max(rms) - np.min(rms))
    energy_variation = 100 - (np.std(rms))*100
    #print("Energy variation is ", energy_variation)

    #mfccs variation
    mfccs = librosa.feature.mfcc(y=amplitudes)[0]
    mfccs = (mfccs - np.min(mfccs))/(np.max(mfccs) - np.min(mfccs))
    mfcc_variation = 100 - (np.std(mfccs))*100
    #print("MFCC variation is ", mfcc_variation)

    #wpm variation
    wpm_std = np.std(sentence_wpm)
    wpm_variation = max(100 - (wpm_std/max_std_wpm)*100, 40)
    
    result["pitch_variation"] = pitch_variation
    result["energy_variation"] = energy_variation
    result["mfcc_variation"] = mfcc_variation
    result["wpm_variation"] = wpm_variation
    return result
    
    