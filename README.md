# Gender Recognition by Voice (ML Model)

Predicts whether a speaker is **male or female** from a voice recording. Includes a Tkinter desktop app: press the 🎤 button, speak, and the model predicts the gender.

## How it works

1. **Audio collection:** voice clips converted to `.wav` (`m4a to wav convert .py`)
2. **Feature extraction:** acoustic features computed with `librosa` and `scipy` (frequency statistics, kurtosis and more)
3. **Model training** (`Model creat/Creat model .ipynb`):
   - Decision Tree, Logistic Regression, Random Forest
   - Class balancing with imbalanced-learn
   - Cross-validation to compare models
   - Best model saved with `joblib`
4. **Prediction app** (`Tkinter Use/round.py`): records from the microphone with PyAudio, extracts the same features, and shows the prediction

## Project structure

```
├── Model creat/      # Dataset handling and model training notebooks
├── model test/       # Testing the saved model on sample voices
├── Tkinter Use/      # Desktop app for live recording and prediction
├── Wavs/             # Sample audio files
├── concatenated_file.csv   # Extracted feature dataset
└── main.py           # CSV preprocessing helper
```

## How to run

```bash
git clone https://github.com/ovibaridar/Gender_Recognition_by_voice_with_model.git
cd Gender_Recognition_by_voice_with_model
pip install numpy pandas scipy librosa scikit-learn imbalanced-learn joblib pyaudio seaborn matplotlib
cd "Tkinter Use"
python round.py   # loads the trained Random Forest model (test_with_rnc)
```

**Stack:** Python · librosa · scikit-learn · imbalanced-learn · PyAudio · Tkinter
