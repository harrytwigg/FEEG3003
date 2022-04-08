import datetime
from importlib.resources import path
from pathlib import Path
import subprocess
from typing import List, Union
from spleeter.separator import Separator


def append_to_log_file(message: str, start_time: str):

    with open(f"log{start_time}.txt", 'a') as log_file:
        # Append message to log file
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        formatted_message = f"{current_time}: {message}\n"
        print(formatted_message)
        log_file.write(formatted_message)


def seperate_artists(names: Union[str, List[str]]):
    start_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if isinstance(names, str):
        names = [names]

    input_paths: List[Path] = []
    output_paths: List[Path] = []

    for name in names:
        path = Path('.').parent.joinpath('downloads', name)

        # If path doesnt exist, throw error
        if not path.exists():
            append_to_log_file(
                f"Artist '{name}' does not exist in downloads folder", start_time)

        # Make output folder if it doesnt exist
        output_path_root = Path('.').parent.joinpath('outputs')
        if not output_path_root.exists():
            output_path_root.mkdir()

        # Recursively search for mp3 files in path

        for file_path in path.glob('**/*'):
            # if file_path is a directory, skip it
            if file_path.is_dir():
                continue

            # Check if file is a mp3 file
            if file_path.suffix != '.mp3':
                continue

            # Save file path to input_path, maintain file ending
            input_paths.append(file_path)

            output_path = output_path_root.joinpath(
                file_path.relative_to(*file_path.parts[:1]))
            output_paths.append(
                output_path.parent.joinpath(str(output_path.stem)))

    seperator = Separator('spleeter:2stems')
    
    def must_process(input_path: Path, output_path: Path):
        try:
            return seperator.separate_to_file(str(input_path), str(output_path))
        except Exception as e:
            print(e)
            append_to_log_file(
                f"Error seperating '{str(input_path)}' to {str(output_path)}", start_time)
            return must_process(input_path, output_path)

    length = len(input_paths)

    for index, paths in enumerate(zip(input_paths, output_paths)):
        input_path, output_path = paths
        progress = round(index / len(input_paths) * 100, 2)

        # Check if wav files already exist in output path
        should_process = True
        
        found_accompaniment = False
        found_vocals = False
        
        for path in output_path.glob('**/*'):
            # Check if file is named accompaniment.wav or vocals.wav
            if path.stem == "accompaniment":
                found_accompaniment = True
            elif path.stem == "vocals":
                found_vocals = True
            if found_vocals and found_accompaniment:
                should_process = False
                break

        if should_process:
            append_to_log_file(
                f"({progress}% {index}/{len(input_paths)}) Separating {input_path.stem}", start_time)
            must_process(input_path, output_path)
        else:
            append_to_log_file(
                f"({progress}% {index}/{len(input_paths)}) Skipping {input_path.stem}", start_time)

            
        
        