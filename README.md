# Google speech to syllables
Script for transcribing audio files into syllables using Google Cloud and Pyphen library. See
[google python tutorial](https://codelabs.developers.google.com/codelabs/cloud-speech-text-python3#0)
and [Pyphen](https://pypi.org/project/Pyphen/). 

Developed at FEE CTU in Prague.

## Use
Process speech audio files and outputs its syllables and corresponding timestamps.
## Setup
* Create a google cloud account
* Create a credentials file for server authentication (hardest step probably)
* Create a new _bucket_ (folder) on the cloud storage
* Upload files of interest to the given bucket
* Run the script `speech-to-words-to-syllables.py` in terminal with the following arguments supplied (within the script):
  * path to the credentials file
  * path to the output folder
  * name of the bucket on google cloud
