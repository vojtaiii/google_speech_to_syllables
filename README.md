# Google speech to syllables
Script for transcribing audio files into syllables using Google Cloud and Pyphen library. See
[google python tutorial](https://codelabs.developers.google.com/codelabs/cloud-speech-text-python3#0)
and [Pyphen](https://pypi.org/project/Pyphen/). 

Developed at FEE CTU in Prague.

## Use
Process speech audio files and outputs its syllables and corresponding timestamps.

```shell
python speech-to-words-to-syllables.py
```

## Setup
* Create a google cloud account
* Create a credentials file for server authentication (hardest step probably)
* Create a new _bucket_ (folder) on the cloud storage
* Upload files of interest to the given bucket
* Run the script `speech-to-words-to-syllables.py` in terminal with the following arguments supplied (within the script):
  * path to the credentials file
  * path to the output folder
  * name of the bucket on google cloud

```python
# set the credentials environment variable
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'C:\\Users\\username\\google_credentials_file.json'
#  files for result storing
output_file_path = 'C:/Users/username/python_project/data_output/'
# obtain the desired bucket
bucket_name = "bucket_name"
```

* Modify the `config` variables to reflect your data

Set the audio sampling rate and language. For Google API:

```python
config = speech.RecognitionConfig(
        sample_rate_hertz=48000,
        language_code="cs-CZ",
        enable_word_time_offsets=True,
    )
```

For Pyphen:

```python
pyphen.language_fallback("cs_CZ")
dic = pyphen.Pyphen(lang='cs_CZ')
```
