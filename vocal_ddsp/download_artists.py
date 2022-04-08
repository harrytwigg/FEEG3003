import csv
from vocaliser.downloader import download_artist
from pathlib import Path


def process_artists_file():
    path = Path('.').parent.joinpath('Artists.csv')

    def get_row():
        with open(path, 'r') as f:
            reader = csv.reader(f)
            # Read first row
            return next(reader)

    def delete_row():
        """Deletes first row from csv"""

        with open(path, 'r') as f:
            reader = csv.reader(f)
            # Read first row
            next(reader)
            # Write remaining rows
            with open(path, 'w') as f:
                writer = csv.writer(f)
                for row in reader:
                    writer.writerow(row)

    while True:
        try:
            row = get_row()
        except StopIteration:
            print('No more artists to download')
            break
        
        download_artist(row[0], row[1])
        delete_row()

if __name__ == '__main__':
    process_artists_file()
