import numpy as np
import pandas as pd
import calculate_confidence_score_acoustic
import confidence_score_transcribe
import calculate_deepness
import calculate_monotonicity


def aggregate_json(dict_, start_point=0):
    for key, value in dict_.items():
        start_point+=value
    return start_point
        
        

audio_name = "full_confidence_1.mp3"
gender = "M"

###confidence score acoustic###
confidence_score_acoustic_json = calculate_confidence_score_acoustic.calculate_confidence_score_acoustic(audio_name)
print("confidence score acoustic is ", confidence_score_acoustic_json)

###confidence score transcribe###
confidence_score_transcribe_json = confidence_score_transcribe.calculate_score_confidence_transcribe(audio_name)
print("confidence score transcribe is ", confidence_score_transcribe_json)

###deepness score###
deepness_score_json = calculate_deepness.calculate_deepness_attractiveness_praat(audio_name, gender)
print("deepness score ", deepness_score_json)
###monotonicity score ###
monotonicity_score_json = calculate_monotonicity.calculate_monotonicity_score(audio_name, confidence_score_transcribe_json["segment_wpm_list"])
print("Monotonicity score ", monotonicity_score_json)


confidence_score_final = aggregate_json(confidence_score_acoustic_json)
confidence_score_transcribe_json.pop('segment_wpm_list')
confidence_score_final = aggregate_json(confidence_score_transcribe_json, confidence_score_final)
confidence_score_final = confidence_score_final/(len(confidence_score_acoustic_json)+len(confidence_score_transcribe_json))

deepness_score_final = deepness_score_json['deepness']
monotonicity_score_final = aggregate_json(monotonicity_score_json)/len(monotonicity_score_json)


print("Final confidence score is ", confidence_score_final)
print("Final deepness score is ", deepness_score_final)
print("Final Monotoncity score is ", monotonicity_score_final)
