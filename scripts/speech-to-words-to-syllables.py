"""
Uses google Speech-to-Text cloud platform for transcription of a audio file into words.
https://cloud.google.com/speech-to-text
The single words are then split into syllables using the PYPHEN module, utilizing HUNSPELL dictionaries
https://pyphen.org/
https://github.com/Kozea/Pyphen
For now, the files have to be located on the cloud with a given URI. Problems emerge when uploading large files from
local storage.

Package names:
google-cloud-speech
google-cloud_storage
pyphen

January 2021
Vojtech Illner
vojtech.illner@fel.cvut.cz
CTU FEE in Prague
"""

from google.cloud import speech
from google.cloud import storage
import os
import pyphen

"""
These three arguments have to be supplied to the script in order to properly work.
For language change dig into pyphen commands in the script.
"""
# set the credentials environment variable
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'C:\\Users\\username\\google_credentials_file.json'
#  files for result storing
output_file_path = 'C:/Users/username/python_project/data_output/'
# obtain the desired bucket
bucket_name = "bucket_name"

# connect to the storage client
# the library will look for credentials in the environment
storage_client = storage.Client()

bucket = storage_client.get_bucket(bucket_name)

# obtain list of all the blobs in the bucket
bucket_list = list(storage_client.list_blobs(bucket))

# cycle through the files
for blob in bucket_list:

    # obtain the current blob name
    blob_name = blob.name
    # get the blobs URL
    link = 'gs://' + bucket_name + '/' + blob_name

    # begin the speech to text transcription
    speech_client = speech.SpeechClient()

    # specify the audio and its specification, together with options for transcription
    audio = speech.RecognitionAudio(uri=link)
    config = speech.RecognitionConfig(
        sample_rate_hertz=48000,
        language_code="cs-CZ",
        enable_word_time_offsets=True,
    )

    # running the speech-to-text operation
    operation = speech_client.long_running_recognize(config=config, audio=audio)
    print("Running speech-to-text on " + blob_name + "...")

    # retrieve the output
    output = operation.result()

    filename1 = output_file_path + blob_name + '_syllables.txt'
    filename2 = output_file_path + blob_name + '_timestamps.txt'

    # result needs to be processed by single results
    output_results = output.results
    syllable_count = 0
    confidence_incremented = 0
    for i in range(len(output_results)):
        # process the output and store it in a single python variable
        output = output_results[i].alternatives  # take the i-th part of the result
        transcript = output[0].transcript  # the transcript
        confidence = output[0].confidence  # confidence of the transcription (only informative measure)
        words = []
        start_times = []
        end_times = []
        for word_info in output[0].words:  # put words and their offsets into lists
            word = word_info.word
            start_time = word_info.start_time.total_seconds()
            end_time = word_info.end_time.total_seconds()

            words.append(word)
            start_times.append(start_time)
            end_times.append(end_time)
        transcription = {  # contains all the info about the audio transcription if i-th result part
            'name': blob_name,
            'transcript': transcript,
            'confidence': confidence,
            'words': words,
            'start_times': start_times,
            'end_times': end_times
        }

        # syllabification part
        # use czech language dictionary
        pyphen.language_fallback("cs_CZ")
        dic = pyphen.Pyphen(lang='cs_CZ')

        syllables_stream = []
        timestamps_stream = []
        print("Running syllabification on " + str(i) + "th part of file...")
        # iterate over the recognized words
        for ii in range(len(transcription.get('words'))):
            word = transcription.get('words')[ii]
            start_time = transcription.get('start_times')[ii]
            end_time = transcription.get('end_times')[ii]

            word_syllables = dic.inserted(word)  # syllabify
            word_syllables = word_syllables.split('-')  # split into a list
            syllables_stream = syllables_stream + word_syllables
            numSyl = len(word_syllables)  # number of syllables in the word

            # single syllables timestamps
            # NAIVE APPROACH (!) but unfortunately I see no other way
            # the timestamps are uniformly distributed across the word
            time_increment = (end_time - start_time) / numSyl
            for iii in range(numSyl):
                timestamp = start_time + iii * time_increment
                timestamps_stream.append(timestamp)

        # filename1 - syllables
        with open(filename1, 'a', encoding="utf-8") as f:
            for syllable in syllables_stream:
                f.write("%s\n" % syllable)
        f.close()
        # filename2 - timestamps
        with open(filename2, 'a') as f:
            for timestamp in timestamps_stream:
                f.write("%f\n" % timestamp)
        f.close()

        # increment some statistics
        syllable_count = syllable_count + len(syllables_stream)
        confidence_incremented = confidence_incremented + confidence
        # file duration - last time stamp
        with open(filename2, 'r') as f:
            lines = f.read().splitlines()
            last_timestamp = lines[-1]
        f.close()

    # display some summary in the terminal
    confidence_overall = confidence_incremented / (len(output_results))
    print("Process finished, files saved.")
    print("Confidence: " + str(confidence_overall) + ", total number of syllables: " + str(syllable_count) + \
          ", duration: " + last_timestamp)
