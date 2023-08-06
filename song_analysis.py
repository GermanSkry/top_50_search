import os
import re
import numpy as np
import heapq
import json
import datetime
import time
import psutil

# Function to read the log file in chunks and filter out invalid rows using a generator
def read_log_file(file_path, chunk_size=1024):
    with open(file_path, 'r') as file:
        buffer = ''
        while True:
            chunk = file.read(chunk_size)
            if not chunk:
                break

            buffer += chunk
            rows = buffer.split('\n')
            buffer = rows.pop()

            for row in rows:
                row = row.strip()
                # Use regex to check if the row follows the correct format
                if re.match(r'^\d+\s*\|\s*\d+\s*\|\s*[A-Z]{2}$', row):
                    yield row

def calculate_all_songs_per_country(filtered_rows):
    songs_per_country = {}
    # Loop through the filtered rows and extract song IDs, user IDs, and the number of streams
    for row in filtered_rows:
        song_id, user_id, country = map(str.strip, row.split('|'))  # Extract song_id, user_id, and country from the row

        # Create a dictionary for each country if it doesn't exist
        if country not in songs_per_country:
            songs_per_country[country] = []

        # Append the streams count for the current song to the corresponding country's array
        songs_per_country[country].append(int(song_id))

    # Write intermediate results to disk for each country using JSON serialization
    countries = list(songs_per_country.keys())  # Create a list with all the countries
    for country in countries:
        songs = songs_per_country[country]
        with open(f"all_songs_intermediate_{country}.json", 'w') as file:
            json.dump(songs, file)

    # Free up memory by deleting the unnecessary variable
    del songs_per_country

    return countries

# Function to write the top 50 songs for each country to separate files
def calculate_top_50_songs_from_files(countries):
    top_50_songs_per_country = {}
    current_date = datetime.date.today().strftime("%Y%m%d")

    for country in countries:
        intermediate_file_path = f"all_songs_intermediate_{country}.json"
        
        if os.path.exists(intermediate_file_path):
            with open(intermediate_file_path, 'r') as file:
                songs = json.load(file)

            song_ids, play_counts = np.unique(songs, return_counts=True)
            top_indices = np.argsort(play_counts)[-50:]
            top_50_songs = [(song_ids[i], play_counts[i]) for i in top_indices]
            top_50_songs_per_country[country] = top_50_songs
        else:
            # Handle cases where the intermediate file is missing or empty
            top_50_songs_per_country[country] = []

    return top_50_songs_per_country
    
def write_top_50_songs_to_files(top_50_songs_per_country):
    current_date = datetime.date.today().strftime("%Y%m%d")
    for country, top_50_songs in top_50_songs_per_country.items():
        filename = f"country_top50_{country}_{current_date}.txt"
        with open(filename, 'w') as file:
            file.write(f"{country}|")
            song_data = ','.join([f"{song}:{count}" for song, count in top_50_songs])
            file.write(song_data)

# Main function to run the entire process
def main():
    start_time = time.time()
    current_date = datetime.date.today().strftime("%Y%m%d")
    file_name = f'listen-{current_date}.log'
    log_file_path = os.path.join('C:/Users/skrge/', file_name)
    filtered_rows = read_log_file(log_file_path)
    countries = calculate_all_songs_per_country(filtered_rows)
    top_50_songs_per_country = calculate_top_50_songs_from_files(countries)
    write_top_50_songs_to_files(top_50_songs_per_country)

    end_time = time.time()

    # Calculate execution time
    execution_time = end_time - start_time

    # Get memory usage
    process = psutil.Process(os.getpid())
    memory_usage = process.memory_info().rss / 1024 / 1024  # Convert to MB

    print(f"Execution time: {execution_time:.2f} seconds")
    print(f"Memory usage: {memory_usage:.2f} MB")

if __name__ == "__main__":
    main()
