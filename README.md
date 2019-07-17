# PyQuake
## A Python Package for Seismic Sonification

PyQuake is a lightweight Python package for seismic sonification that uses the [IRIS Timeseries API](http://service.iris.edu/irisws/timeseries/1/) to retrieve seismic data and convert it into audio. This package exists mainly as a modular extension of the [Earthtunes](https://github.com/cooperbarth/Earthtunes) project.

Download: `python3 -m pip install pyquake`

## Code Example:
```
import pyquake as pq, datetime

IU_stations = pq.getStations(network="IU")
closest_IU_station = pq.getNearestStation(34.94, -106.45, IU_stations)

header, raw_data = pq.getRawData(closest_IU_station, datetime.datetime(2019, 6, 1), duration=3600)
_ = pq.generateAudioFile(raw_data, soundname=f"{repr(closest_IU_station)}_audio", amp_level=0.8)
```

### The *SeismicStation* class
- *network*: Network code used by the station. 
- *station*: Station code for the station.
- *location* (OPTIONAL): Regional location code for the seismic station.
- *name* (OPTIONAL): An optional alias for the station.
- *latitude* (OPTIONAL): The latitude of the station. Defaults to 0.0.
- *longitude* (OPTIONAL): The longitude of the station. Defaults to 0.0.


## Station Retrieval:

### *getStations*
Returns stations in the IRIS Database with the given Network or Station codes.
#### Parameters:
- *network* (OPTIONAL): Network code used by the station.
- *station* (OPTIONAL): Station code for the station.
#### Returns:
- An array of SeismicStation objects.

### *getAllStations*
Returns all stations in the IRIS Database. *Note: This is an alias for calling `makeIrisStationRequest` or `getStations` with no parameters.*
#### Returns:
- An array of SeismicStation objects.

### *makeIrisStationRequest*
Makes a GET request to the IRIS station database. *This function is called by the above function. You shouldn't call this manually unless you really know what you're doing.*

### *getNearestStation*
Returns the nearest IRIS station to a given coordinate.
#### Parameters:
- *latitude*: Input latitude.
- *longitude*: Input longitude.
- *stations*: An array of SeismicStation objects to search.
#### Returns:
- A SeismicStation object.


## Seismic Data Retrieval:

### *getRawData*
Returns the raw data from the seismic station during the specified timeframe. If the location code in the seismic station isn't specified, it will try several different codes in an attempt to find data.
#### Parameters:
- *seismic_station*: The seismic station object representing the station from which to pull data.
- *start_datetime*: The datetime at which the audio sample should begin.
- *duration* (OPTIONAL): The length of the desired sample, in real-time seconds. Defaults to 3600 (1 hour).
- *channel* (OPTIONAL): The channel from which the data is taken. This is currently limited to the BHZ and LHZ channels and defaults to BHZ.
#### Returns:
- A tuple containing the header for the IRIS response and an array containing the magnitude sound data.

### *generateAudioFile*
#### Parameters:
- *sound_array*: The magnitude sound array to convert to audio.
- *sampling_rate*: The sampling rate that the output audio should use. NOTE: The input audio is taken at a very low sample rate; this parameter should be set to a normallized sample rate (default 44100) to prevent long files. *If using LHZ, this sample rate should be dropped to around 1100 to account for the lower sampling rate of the LHZ channel.*
- *soundname*: The filename (or path+filename) at which to save the output .wav file. The ".wav" extension can be included or excluded. Defaults to "pyquake_audio".
- *amp_level*: A scaling factor to control track amplitude, and thus relative volume. Falls between 0 (exclusive) and 1 (inclusive). Defaults to 1.
#### Returns:
- The scaled audio array (of equal length to the input array).
