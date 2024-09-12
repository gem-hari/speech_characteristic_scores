import numpy as np
import pandas as pd
import calculate_confidence_score_acoustic
import confidence_score_transcribe
import calculate_deepness
import calculate_monotonicity
import calculate_strength
import calculate_musculanity
import calculate_feminity
import time
import concurrent.futures

def aggregate_json_weight(dict_, dict_weight_=None):
    numerator = 0
    denominator = 0
    for key, value in dict_.items():
        if dict_weight_ is not None and key in dict_weight_:
            numerator+= value*dict_weight_[key]
            denominator+= dict_weight_[key]
        else:
            numerator+= value
            denominator+=1
    return numerator/denominator
    
audio_name = "full_confidence_1.mp3"
gender = "M"

weight_confidence_transcribe = {"mean_filler_score":3.0, "mean_speed_score":2.0,"calculate_pause_score":2.0}
weight_confidence_acoustic = {"filled_pause_score":2.0,"partial_word_score":2.0,"repetition_score":2.0,"restart_score":1.0}
weight_monotonicity = {"pitch_variation":2.0, "energy_variation":2.0,"wpm_variation":1.0}

"""
###confidence score acoustic###
start_time = time.time()
confidence_score_acoustic_json = calculate_confidence_score_acoustic.calculate_confidence_score_acoustic(audio_name, save_result_df= False)
end_time = time.time()
print("confidence score acoustic is ", confidence_score_acoustic_json)
print("Total time taken is " , end_time-start_time)

###confidence score transcribe###
confidence_score_transcribe_json = confidence_score_transcribe.calculate_score_confidence_transcribe(audio_name)
print("confidence score transcribe is ", confidence_score_transcribe_json)
"""

with concurrent.futures.ThreadPoolExecutor() as executor:
    future_acoustic = executor.submit(calculate_confidence_score_acoustic.calculate_confidence_score_acoustic,audio_name)
    future_transcribe = executor.submit(confidence_score_transcribe.calculate_score_confidence_transcribe,audio_name)

confidence_score_acoustic_json = future_acoustic.result()
confidence_score_transcribe_json = future_transcribe.result()

    
###deepness score###
deepness_score_json = calculate_deepness.calculate_deepness_attractiveness_praat(audio_name, gender)
print("deepness score ", deepness_score_json)
###monotonicity score ###
monotonicity_score_json = calculate_monotonicity.calculate_monotonicity_score(audio_name, confidence_score_transcribe_json["segment_wpm_list"])
print("Monotonicity score ", monotonicity_score_json)
confidence_score_transcribe_json.pop('segment_wpm_list')


confidence_score_acoustic_final = aggregate_json_weight(confidence_score_acoustic_json,weight_confidence_acoustic)
confidence_score_transcribe_final = aggregate_json_weight(confidence_score_transcribe_json, weight_confidence_transcribe)
confidence_score_final = (confidence_score_acoustic_final+confidence_score_transcribe_final)/2

deepness_score_final = deepness_score_json['deepness']
monotonicity_score_final = aggregate_json_weight(monotonicity_score_json, weight_monotonicity)


strength_score_json = calculate_strength.calculate_strength(audio_name)
print("Strength score ", strength_score_json)
strength_score_final = strength_score_json["strength_score"]


if gender=="M":
    musculanity_score_json = calculate_musculanity.calculate_musculanity(audio_name)
    print("Masculanity score is ", musculanity_score_json)
    musculanity_score_final = musculanity_score_json["musculanity_score"]
else:
    feminity_score_json = calculate_feminity.calculate_feminity(audio_name)
    print("Feminity score is ", feminity_score_json)
    feminity_score_final = feminity_score_json["feminity_score"]

print("Final confidence score acoustic is ", confidence_score_acoustic_final)
print("Final confidence score statistics is ", confidence_score_transcribe_final)

print("*****Final scores*****")
print("Final confidence score is ", confidence_score_final)
print("Final deepness score is ", deepness_score_final)
print("Final Monotonicity score is ", monotonicity_score_final)
print("Final strength score is ", strength_score_final)
if gender=="M":
    print("Final Masculanity score is ", musculanity_score_final)
else:
    print("Final Feminity score is ", feminity_score_final)