import urllib.request as urllib
import datetime
import numpy as np
from scipy.io import wavfile

supported_locations = {
    'chile': {
        'network': 'IU',
        'station': 'LCO',
        'location': '10'
    }
}

def getRawData(location_name, start_datetime, duration=3600, channel='BHZ'):
    '''
    Params:
    -location: name of location to map to station info
    -start_datetime: datetime object from which the sample should be taken
    -duration: (OPTIONAL) duration of the sample in seconds
    -channel: (OPTIONAL) channel from which the data is taken (controls # of points)

    Returns:
    -An tuple containing an the header for the response and an array containing the magnitude sound data at each time interval
    '''

    def isNumber(num):
        try:
            float(num)
            return True
        except:
            return False

    assert location_name in supported_locations, location_name + " is not a supported location."
    assert isNumber(duration), "Please enter a valid duration."

    station_info = supported_locations[location_name]
    network = '?net=' + station_info['network']
    station = "&sta=" + station_info['station']
    location = "&loc=" + station_info['location']
    channel = "&cha=" + channel

    date = "&starttime=" + str(start_datetime.date())
    time = "T" + str(start_datetime.time()).split('.')[0]

    iris_url_header = "http://service.iris.edu/irisws/timeseries/1/query"
    iris_body = network + station + location + channel
    iris_datetime = date + time + "&duration=" + str(int(duration))
    iris_footer = "&demean=true&scale=auto&output=ascii1"
    iris_url = iris_url_header + iris_body + iris_datetime + iris_footer

    print("Requesting data from IRIS...")
    ws = urllib.urlopen(iris_url)

    print("Loading Data...")
    df = ws.read().decode()
    dflines = df.split('\n')

    return dflines[0], [float(i) for i in dflines[1:] if isNumber(i)]

def generateSoundFile(sound_array, sampling_rate=44100, soundname='pyquake_audio', amp_level=1):
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

    scaled_amp = max(sound_array) * amp_level
    sound = np.asarray(sound_array)
    scaled_audio = (2**31) * np.arctan(sound / scaled_amp) / (0.5 * np.pi)
    s32 = np.int32(scaled_audio)

    if (".wav" not in soundname):
        soundname += ".wav"
    print("Creating audio file...")
    wavfile.write(soundname, int(sampling_rate), s32)

    return s32