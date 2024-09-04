import pandas as pd
import numpy as np
import librosa
import torch, torchaudio
import warnings
from transformers import Wav2Vec2FeatureExtractor
warnings.filterwarnings("ignore")
from models import AcousticModel, MultimodalModel
labels = ['FP', 'RP', 'RV', 'RS', 'PW']

def run_acoustic_based(audio_file, device="cpu"):
    # Load audio file and resample to 16 kHz
    #audio, orgnl_sr = torchaudio.load(audio_file)
    audio , orgnl_sr = librosa.load(audio_file)
    audio = torch.tensor(audio.reshape(1,-1))
    audio_rs = torchaudio.functional.resample(audio, orgnl_sr, 16000)[0, :]
    feature_extractor = Wav2Vec2FeatureExtractor(feature_size=1,
                                                 sampling_rate=16000,
                                                 padding_value=0.0,
                                                 do_normalize=True,
                                                 return_attention_mask=False)
    audio_feats = feature_extractor(audio_rs, sampling_rate=16000).input_values[0]
    audio_feats = torch.Tensor(audio_feats).unsqueeze(0)
    audio_feats = audio_feats.to(device)

    # Initialize WavLM model and load in pre-trained weights
    model = AcousticModel()
    model.load_state_dict(torch.load('demo_models/acoustic.pt', map_location='cpu'))
    model.to(device)
    print('loaded finetuned acoustic model') 

    # Get WavLM output
    emb, output = model(audio_feats)
    probs = torch.sigmoid(output)
    preds = (probs > 0.5).int()[0]
    emb = emb[0]

    return emb, preds



def calculate_confidence_score_acoustic(audio_path, multi_factor=7, save_result_df= False):
    _, preds = run_acoustic_based(audio_path)
    pred_df = pd.DataFrame(preds.cpu(), columns=labels).astype(int)
    pred_df['frame_time'] = [round(i * 0.02, 2) for i in range(pred_df.shape[0])]
    pred_df = pred_df.set_index('frame_time')
    
    result={}
    df = pred_df
    if save_result_df:
        df.to_csv(audio_path+"_acoustic_frame_prediction.csv", index=True) 
        print("Saved frame level prediction at ",audio_path+"_acoustic_frame_prediction.csv")       
    len_df = len(df)
    
    result["filled_pause_score"] = max(40,((len_df - multi_factor*df["FP"].sum())/len(df))*100)
    result["partial_word_score"] = max(40,((len_df - multi_factor*df["RP"].sum())/len(df))*100)
    result["repetition_score"] = max(40,((len_df - multi_factor*df["RV"].sum())/len(df))*100)
    #revision score is not predicting well
    #result["revision_score"] = max(40,((len_df - multi_factor*df["RS"].sum())/len(df))*100)
    result["restart_score"] = max(40,((len_df - multi_factor*df["PW"].sum())/len(df))*100)
    return result  
#print(calculate_confidence_score_acoustic("motivationalsample1.wav"))