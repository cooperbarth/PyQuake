import urllib.request as urllib
import datetime
import numpy as np
from scipy.io import wavfile

# GSN Stations: https://earthquake.usgs.gov/monitoring/operations/network.php?virtual_network=GSN
# IRIS DMC: https://ds.iris.edu/cgi-bin/seismiquery/bin/station.pl
class SeismicStation:
    def __init__(self, network, station, location="", name="", latitude=0.0, longitude=0.0):
        self.network = network
        self.station = station
        self.name = name
        self.location = location
        self.latitude = latitude
        self.longitude = longitude
    
    def __repr__(self):
        return self.name if self.name != '' else self.network
#location may be specified if they want to check a specific one, otherwise it should loop yhrough --, 00, 10, 20
#Example: https://ds.iris.edu/mda/IU/ANMO/?starttime=1989-08-29&endtime=2599-12-31

#Takes in station and time info and returns an array representation of audio.
def getRawData(seismic_station, start_datetime, duration=3600, channel='BHZ'):
    '''
    Params:
    -seismic_station: (SEISMIC_STATION OBJECT) seismic station object
    -start_datetime: (DATETIME OBJECT) datetime object from which the sample should be taken
    -duration: (INT, OPTIONAL) duration of the sample in seconds
    -channel: (STRING, OPTIONAL) channel from which the data is taken (controls # of points)

    Returns:
    -A tuple containing the header for the IRIS response and an array containing the magnitude sound data.
    '''

    supported_locations = ["--", "00", "10", "20"]
    def isNumber(num):
        try:
            float(num)
            return True
        except:
            return False

    assert seismic_station.network and seismic_station.station, "seismic_station must be a valid instance of the SeismicStation class."
    assert isinstance(start_datetime, datetime.datetime), "start_datetime must be a datetime created via the Python datetime module."
    assert start_datetime < datetime.datetime.now(), "start_datetime cannot be in the future."
    assert isNumber(duration), "Please enter a valid duration."
    assert float(duration) < 2_592_000, "Time series requested must not exceed 30 days."
    assert channel in ["BHZ", "LHZ"], "Only BHZ and LHZ channels are supported."

    network = f"?net={seismic_station.network}"
    station = f"&sta={seismic_station.station}"
    locations = supported_locations if seismic_station.location not in supported_locations else [seismic_station.location]
    channel = f"&cha={channel}"

    date = "&starttime=" + str(start_datetime.date())
    time = "T" + str(start_datetime.time()).split('.')[0]

    iris_url_header = "http://service.iris.edu/irisws/timeseries/1/query"
    iris_datetime = date + time + "&duration=" + str(int(duration))
    iris_footer = "&demean=true&scale=auto&output=ascii1"

    print(f"Requesting data from IRIS...")
    ws = None
    for location in locations:
        if len(locations) > 1:
            print(f"Trying location {location} for station {seismic_station.station}...")
        iris_body = network + station + f"&loc={location}" + channel
        iris_url = iris_url_header + iris_body + iris_datetime + iris_footer
  
        try:
            ws = urllib.urlopen(iris_url)
            break
        except:
            continue
    if ws is None:
        raise Exception("ERROR: Could not retrieve data from IRIS.")

    print("Loading Data...")
    try:
        df = ws.read().decode()
        dflines = df.split('\n')
    except:
        raise Exception("ERROR: Data could not be parsed.")

    return dflines[0], [float(i) for i in dflines[1:] if isNumber(i)]

#Saves an audio file generated from an array representation to the working directory
def generateAudioFile(sound_array, sampling_rate=44100, soundname='pyquake_audio', amp_level=1):
    '''
    Params:
    -sound_array: array of points representing a sound wave
    -sampling_rate: (OPTIONAL) number of samples per second to represent
    -soundname: (OPTIONAL) path to location and name of .wav file
    -amp_level: (OPTIONAL) modifier used to manipulate audio amplitude level

    Returns:
    -A scaled audio array containing the magnitude sound data at each time interval
    '''
    assert amp_level <= 1 and amp_level > 0, 'Amplitude Level must be greater than 0 and less than or equal to 1.'

    max_point = max(sound_array)
    if (len(sound_array)) <= 2:
        print("WARNING: The function getRawData returns a tuple containing the request header and the audio array. Make sure to pass in the correct value.")
        return
    scaled_amp = max(sound_array) * amp_level
    sound = np.asarray(sound_array)
    scaled_audio = (2**31) * np.arctan(sound / scaled_amp) / (0.5 * np.pi)
    s32 = np.int32(scaled_audio)

    if (".wav" not in soundname):
        soundname += ".wav"
    print("Creating audio file...")
    wavfile.write(soundname, int(sampling_rate), s32)

    return s32

station = SeismicStation('IU', 'ANMO')
header, arr = getRawData(station, datetime.datetime(2019, 6, 1))
wav = generateAudioFile(arr)