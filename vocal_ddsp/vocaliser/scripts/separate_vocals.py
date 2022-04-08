import imp
from pathlib import Path
import shutil
import glob
import os


def copy_vocals_wav(artist: str):
    """Seperates vocals.wav from accompaniment.wav, will move files"""
    
    # Get path to downloads folder
    artist_path = Path('.').parent.joinpath('outputs').joinpath(artist)
    
    separated_root_path = Path('.').parent.joinpath('separated')
    
    if not separated_root_path.exists():
        separated_root_path.mkdir()
    
    separated_path = separated_root_path.joinpath(artist)
    
    # If seperated folder doesnt exist at path, create it
    if not separated_path.exists():
        separated_path.mkdir()
    
    # Find all vocals.wav files
    pathname = str(artist_path) + "/**/vocals.wav"
    files = glob.glob(pathname, recursive=True)

    # For each file, move it to the seperated folder
    length = len(files)
    for index, file in enumerate(files):
        print(f"{index}/{length}: {file}")
        output = file.replace('outputs', 'separated')
        os.makedirs(os.path.dirname(output), exist_ok=True)
        shutil.move(file, output)
        
        

if __name__ == '__main__':
    copy_vocals_wav('Taylor Swift')