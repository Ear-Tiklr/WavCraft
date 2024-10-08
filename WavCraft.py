import time
import argparse
import sys

import wavcraft.utils as utils
import wavcraft.pipeline as pipeline
from config_utils.config_loader_json import get_config

config = get_config()

parser = argparse.ArgumentParser()
sub_parsers = parser.add_subparsers(dest="mode", help='Type of WavCraft to use')
# Basic mode
basic_parser = sub_parsers.add_parser("basic")
basic_parser.add_argument('-f', '--full', action='store_true', help='Go through the full process')
basic_parser.add_argument('--input-wav', nargs='+', default=[], help='a list of input wave paths')
basic_parser.add_argument('--input-text', type=str, help='input text or text file')
# gpt-4-0125-preview
basic_parser.add_argument('--model', type=str, default=config.get('model', 'gpt-3.5'), help='ChatGPT model.')
basic_parser.add_argument('--session-id', type=str, default='',
                          help='session id, if set to empty, system will allocate an id')
# Inspiration mode
inspire_parser = sub_parsers.add_parser("inspiration")
inspire_parser.add_argument('-f', '--full', action='store_true', help='Go through the full process')
inspire_parser.add_argument('--input-wav', nargs='+', default=[], help='a list of input wave paths')
inspire_parser.add_argument('--input-text', type=str, help='input text or text file')
inspire_parser.add_argument('--model', type=str, default=config.get('model', 'gpt-3.5'), help='ChatGPT model.')
inspire_parser.add_argument('--session-id', type=str, default='',
                            help='session id, if set to empty, system will allocate an id')

args = parser.parse_args()

if args.mode in ("basic", "inspiration"):
    if args.full:
        input_text = args.input_text
        input_wav = args.input_wav

        start_time = time.time()
        session_id = pipeline.init_session(args.session_id)
        api_key = utils.get_api_key()

        assert api_key != None, "Please set your openai_key in the environment variable."

        print(f"Session {session_id} is created.")

        pipeline.full_steps(session_id, input_wav, input_text, api_key, model=args.model, mode=args.mode)
        end_time = time.time()

        print(f"Audio editor took {end_time - start_time:.2f} seconds to complete.")


def main(args):
    if args.mode in ("basic", "inspiration"):
        if args.full:
            input_text = args.input_text
            input_wav = args.input_wav

            start_time = time.time()
            session_id = pipeline.init_session(args.session_id)
            api_key = utils.get_api_key()

            assert api_key is not None, "Please set your openai_key in the environment variable."

            print(f"Session {session_id} is created.")

            pipeline.full_steps(session_id, input_wav, input_text, api_key, model=args.model, mode=args.mode)
            end_time = time.time()

            print(f"Audio editor took {end_time - start_time:.2f} seconds to complete.")


if __name__ == "__main__":
    # Simulate the command-line arguments
    sys.argv = [
        'WavCraft.py',
        'basic',
        '-f',
        '--input-wav', 'assets/duck_quacking_in_water.wav',
        '--input-text', 'Add dog barking.',
        '--session_id', 'your_session_id',
        '--model', 'your_model'
    ]

    parser = argparse.ArgumentParser(description="Audio editor script")
    parser.add_argument("mode", choices=["basic", "inspiration"], help="Mode of operation")
    parser.add_argument("-f", "--full", action="store_true", help="Run in full mode")
    parser.add_argument("--input_text", type=str, help="Input text for processing")
    parser.add_argument("--input_wav", type=str, help="Input WAV file for processing")
    parser.add_argument("--session_id", type=str, required=True, help="Session ID")
    parser.add_argument("--model", type=str, required=True, help="Model to use")

    args = parser.parse_args()
    main(args)
