from scipy.optimize import curve_fit
import parselmouth
import numpy as np
from calculate_deepness import calculate_deepness_attractiveness_praat
### reference is paper https://www.sciencedirect.com/science/article/pii/S0018506X14001639?casa_token=jfOjbLIhqdgAAAAA:oBvuwdvw5YqqiaN4GQ2lwi16qMZtW7CT5WHMHVm91c-IuYEsQ-ATVTfU5167YU-9wIrAOHvi
# Function to fit the formants to the equation Fi = ((2i - 1)/2)*ΔF
def formant_equation(i, delta_f):
    return (2 * i - 1) / 2 * delta_f

# Load sound file and extract formants using Burg method
def get_formants(sound, max_formant=5000, window_length=0.03):
    formant = sound.to_formant_burg(time_step=0.01, max_number_of_formants=5, 
                                    maximum_formant=max_formant, 
                                    window_length=window_length, 
                                    pre_emphasis_from=50)
    return formant

# Extract center frequencies (F1 - F4) from formant object at a specific time
# Calculate average ΔF (formant spacing) using curve fitting

def calculate_delta_f(formant_frequencies):
    i_vals = np.array([1, 2, 3, 4])  # Formant index (1 to 4 for F1-F4)
    popt, _ = curve_fit(formant_equation, i_vals, formant_frequencies)
    delta_f = popt[0]  # Extract the best-fit value for ΔF
    return delta_f

#calculate the formants delta_F using the above functions
def get_formants_delta_F(sound):
    formants = get_formants(sound)
    formant_data = []
    delta_F = []

    for t in np.arange(0, sound.duration, 0.01):
        try:
            f1 = formants.get_value_at_time(1, t)
            f2 = formants.get_value_at_time(2, t)
            f3 = formants.get_value_at_time(3, t)
            f4 = formants.get_value_at_time(4, t)
            formant_frequencies = [f1, f2, f3, f4]

            if all(f is not None for f in formant_frequencies):
              delta_F_time = calculate_delta_f(formant_frequencies)
              delta_F.append(delta_F_time)
        except:
            continue
    return np.array(delta_F)
#return the musculanity score for delta_f based on logic that lower delta_f is more attractive
def masculinity_score_delta_f(delta_f, ref_delta_f=1018, ref_score = 75, tolerance=10):
    if delta_f<ref_delta_f:
      ref_score += (abs(delta_f-ref_delta_f)/tolerance) 
    else:
      ref_score -= (abs(delta_f-ref_delta_f)/tolerance) 
    return ref_score
#entry point to delta_F analysis
def delta_F_analysis(audio_path):
  sound = parselmouth.Sound(audio_path)
  delta_f = get_formants_delta_F(sound)
  delta_f_mean = np.mean(delta_f)
  print("mean delta f ", delta_f_mean)
  score = masculinity_score_delta_f(delta_f_mean)
  return score

def calculate_musculanity(audio_path):
  deepness_dict= calculate_deepness_attractiveness_praat(audio_path, "M")
  deepness_score = deepness_dict["deepness"]
  delta_f_score = delta_F_analysis(audio_path)

  print("deepness score is ", deepness_score)
  print("delta_f_score is ", delta_f_score)

  musculanity_score = (3*deepness_score+2*delta_f_score)/5
  return musculanity_score

print(calculate_musculanity("little_nervous_1.mp3"))