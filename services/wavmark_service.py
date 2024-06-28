import os
import sys
import yaml
import logging
import librosa
import soundfile
import torch
import wavmark
import numpy as np
from flask import Flask, request, jsonify
from scipy.io.wavfile import write

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from wavcraft.utils import get_service_port


with open('wavcraft/configs.yaml', 'r') as file:
    config = yaml.safe_load(file)

# Configure the logging format and level
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Create a FileHandler for the log file
os.makedirs('services_logs', exist_ok=True)
log_filename = 'services_logs/Wav-API.log'
file_handler = logging.FileHandler(log_filename, mode='w')
file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))

# Add the FileHandler to the root logger
logging.getLogger('').addHandler(file_handler)


# Audio watermarking preserved by WavCraft
payload = np.array([0,1,0,1,0,1,1,1,0,1,0,0,0,0,1,1])
model = wavmark.load_model().to("cuda" if torch.cuda.is_available() else 'cpu')
logging.info('WavMark is loaded ...')


app = Flask(__name__)


@app.route('/audio_watermark', methods=['POST'])
def audio_watermark():
    # Receive the text from the POST request
    data = request.json
    wav_path = data['wav_path']
    sample_rate = data.get('sample_rate', 16000)
    action = data.get('action', "encode")
    output_wav = data.get('output_wav', 'out.wav')
    logging.info(f"{action} watermark with {wav_path}...")

    # the audio should be a single-channel 16kHz wav, you can read it using soundfile:
    signal, sr = soundfile.read(wav_path)
    assert sr == sample_rate, "WavMark use 16kHz audio only!"
    # Otherwise, you can use the following function to convert the host audio to single-channel 16kHz format:
    # from wavmark.config_utils import file_reader
    # signal = file_reader.read_as_single_channel(wav_path, aim_sr=sample_rate)

    try:
        assert action in ("encode", "decode")
        if action == "encode":
            watermarked_signal, _ = wavmark.encode_watermark(model, signal, payload, show_progress=True)
            # you can save it as a new wav:
            soundfile.write(output_wav, watermarked_signal, sample_rate)
        else:
            payload_decoded, _ = wavmark.decode_watermark(model, signal, show_progress=True)
            confidence_score = (payload == payload_decoded).mean() * 100
            if confidence_score < 0.5:
                logging.info(f"Audio file {wav_path} is not generated by WavCraft.")
            else:
                logging.info(f"Audio file {wav_path} is generated by WavCraft.")

        # Return success message and the filename of the generated audio
        return jsonify({'message': f"Sucessful {action} watermark with {wav_path}..."})

    except Exception as e:
        # Return error message if something goes wrong
        return jsonify({'API error': str(e)}), 500


if __name__ == '__main__':
    service_port = get_service_port("WAVMARK_SERVICE_PORT")
    # We disable multithreading to force services to process one request at a time and avoid CUDA OOM
    app.run(debug=False, threaded=False, port=service_port)