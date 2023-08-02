import os
import re
import random
import string
import heapq
import pickle
import datetime

# Function to read the log file and filter out invalid rows
def read_log_file(file_path):
    rows = []
    with open(file_path, 'r') as file:
        for line in file:
            row = line.strip()
            # Use regex to check if the row follows the correct format
            if re.match(r'^\d+\s*\|\s*\d+\s*\|\s*[A-Z]{2}$', row):
                rows.append(row)
    return rows

# Function to records all songs for each country and save in intermediate files
def calculate_all_songs_per_country(filtered_rows):
    songs_per_country = {}
    # Loop through the filtered rows and extract song IDs, user IDs, and the number of streams
    for row in filtered_rows:
        song_id, user_id, country = map(str.strip, row.split('|'))  # Extract song_id, user_id, and country from the row

        # Create a dictionary for each country if it doesn't exist
        if country not in songs_per_country:
            songs_per_country[country] = {}

        # Increment the streams count for the current song in the corresponding country
        songs_per_country[country][song_id] = songs_per_country[country].get(song_id, 0) + 1

    # Write intermediate results to disk for each country using pickle serialization
    for country, songs in songs_per_country.items():
        with open(f"all_songs_intermediate_{country}.pkl", 'wb') as file:
            pickle.dump(list(songs.keys()), file)

    return songs_per_country

def calculate_top_50_songs_from_files(all_songs_per_country):
    top_50_songs_per_country = {}
    # Calculate the top 50 songs for each country based on the play count
    for country, songs in all_songs_per_country.items():
        top_50_songs = heapq.nlargest(50, songs, key=lambda x: songs[x])
        top_50_songs_per_country[country] = top_50_songs

    return top_50_songs_per_country

# Function to write the top 50 songs for each country to separate files
def write_top_50_songs_to_files(top_50_songs_per_country):
    current_date = datetime.date.today().strftime("%Y%m%d")
    for country, top_50_songs in top_50_songs_per_country.items():
        filename = f"country_top50_{country}_{current_date}.txt"
        with open(filename, 'w') as file:
            file.write(f"{country}|")
            song_data = ','.join(top_50_songs)
            file.write(song_data)

# Main function to run the entire process
def main():
    current_date = datetime.date.today().strftime("%Y%m%d")
    file_name = f'listen-{current_date}.log'
    log_file_path = os.path.join('C:/Users/skrge/', file_name)
    filtered_rows = read_log_file(log_file_path)
    all_songs_per_country = calculate_all_songs_per_country(filtered_rows)
    top_50_songs_per_country = calculate_top_50_songs_from_files(all_songs_per_country)
    write_top_50_songs_to_files(top_50_songs_per_country)

if __name__ == "__main__":
    main()
