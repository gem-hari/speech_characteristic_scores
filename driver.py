import numpy as np
import pandas as pd
import calculate_confidence_score_acoustic
import confidence_score_transcribe
import calculate_deepness
import calculate_monotonicity

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
    
audio_name = "little_nervous_1.mp3"
gender = "M"

weight_confidence_transcribe = {"mean_filler_score":3.0, "mean_speed_score":2.0,"calculate_pause_score":2.0}
weight_confidence_acoustic = {"filled_pause_score":2.0,"partial_word_score":2.0,"repetition_score":2.0,"restart_score":1.0}
weight_monotonicity = {"pitch_variation":2.0, "energy_variation":2.0,"wpm_variation":1.0}

###confidence score acoustic###
confidence_score_acoustic_json = calculate_confidence_score_acoustic.calculate_confidence_score_acoustic(audio_name, save_result_df= False)
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
confidence_score_transcribe_json.pop('segment_wpm_list')


confidence_score_acoustic_final = aggregate_json_weight(confidence_score_acoustic_json)
confidence_score_transcribe_final = aggregate_json_weight(confidence_score_transcribe_json, weight_confidence_transcribe)
confidence_score_final = (confidence_score_acoustic_final+confidence_score_transcribe_final)/2

deepness_score_final = deepness_score_json['deepness']
monotonicity_score_final = aggregate_json_weight(monotonicity_score_json, weight_monotonicity)


print("Final confidence score acoustic is ", confidence_score_acoustic_final)
print("Final confidence score statistics is ", confidence_score_transcribe_final)
print("Final confidence score is ", confidence_score_final)
print("Final deepness score is ", deepness_score_final)
print("Final Monotoncity score is ", monotonicity_score_final)
