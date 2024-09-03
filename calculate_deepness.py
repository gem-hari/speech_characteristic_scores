#using praat
#medium to high frequency is attractive for women
#low to medium is attractive for men
import parselmouth
from parselmouth.praat import call
from scipy.stats import skewnorm

def calculate_deepness_attractiveness_praat(audio_path, gender="M"):
  result ={}
  if gender == "M":
    f0range = [75,300]
    sound = parselmouth.Sound(audio_path)
    pitch = call(sound, "To Pitch", 0.0, f0range[0], f0range[1])
    avg_f0 = call(pitch, "Get mean", 0, 0, "Hertz")


    mean = 125
    a = -1.0
    scale = 100
    max_pdf = 0.005
  else:
    f0range = [100,500]
    sound = parselmouth.Sound(audio_path)
    pitch = call(sound, "To Pitch", 0.0, f0range[0], f0range[1])
    avg_f0 = call(pitch, "Get mean", 0, 0, "Hertz")

    mean = 200
    a = 3.0
    scale = 50
    max_pdf = 0.0135

  #print("Fundamental frequency obtained is ", avg_f0)

  #calculating the skewness and scale and mean
  loc = mean
  curr_pdf = skewnorm.pdf(avg_f0, a, loc, scale)

  #print("Max pdf is ", max_pdf, " and current pdf is ", curr_pdf)
  deepness_score = 100 * (curr_pdf / (max_pdf))
  #print("deepness attractiveness score is ", deepness_score)
  result["deepness"] = deepness_score
  result["avg_f0"] = avg_f0
  return result

#print(calculate_deepness_attractiveness_praat("stutteringsample.wav", gender="M"))