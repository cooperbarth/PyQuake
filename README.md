# PyQuake
## A Python Library for Seismic Sonification

An easy-to-use open-source Python library for seismic sonification using the IRIS Timeseries Web Service.

Download: `python3 -m pip install pyquake`

## Code Example:
```
import pyquake

seismic_station = pyquake.SeismicStation("IU", "LCO", "10")
header, raw_data = pyquake.getRawData(seismic_station, datetime.datetime(2019, 6, 1), duration=3600)
_ = pyquake.generateAudioFile(raw_data, soundname="chile_seismic_audio", amp_level=0.8)
```

### SeismicStation
- *network*: Network over which to pull the data from. 
- *station*: Code for the station.
- *location*: Regional location code for the seismic station.
*Note: Check that your seismic station is valid at* https://ds.iris.edu/gmap/

### getRawData
##### Parameters:
- *seismic_station*: The seismic station object representing the station from which to pull data.
- *start_datetime*: The datetime at which the audio sample should begin.
- *duration* (OPTIONAL): The length of the desired sample, in real-time seconds. Defaults to 3600 (1 hour).
- *channel* (OPTIONAL): The channel from which the data is taken. This is currently limited to the BHZ and LHZ channels and defaults to BHZ.
##### Returns:
- A tuple containing the header for the IRIS response and an array containing the magnitude sound data.

### generateAudioFile
##### Parameters:
- *sound_array*: The magnitude sound array to convert to audio.
- *sampling_rate*: The sampling rate that the output audio should use. NOTE: The input audio is taken at a very low sample rate; this parameter should be set to a normallized sample rate (default 44100) to prevent long files. *If using LHZ, this sample rate should be dropped to around 1100 to account for the lower sampling rate of the LHZ channel.*
- *soundname*: The filename (or path+filename) at which to save the output .wav file. The ".wav" extension can be included or excluded. Defaults to "pyquake_audio".
- *amp_level*: A scaling factor to control track amplitude, and thus relative volume. Falls between 0 (exclusive) and 1 (inclusive). Defaults to 1.
##### Returns:
- The scaled audio array (of equal length to the input array).

IRIS Timeseries documentation: http://service.iris.edu/irisws/timeseries/1/
Concept pulled from the [Earthtunes](https://github.com/cooperbarth/Earthtunes) project.
