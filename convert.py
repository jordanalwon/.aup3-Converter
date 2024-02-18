from reader import SQLite3Reader
from binary_stream import BinaryStream
from name_space import NameSpace
from xml_object import XMLObject
import numpy as np
import soundfile as sf

class Converter():
    def __init__(self, path):
        # Read .aup3
        self.file = SQLite3Reader(path)

        # Get name-space
        binary_name_space = self.file.binary_name_space()
        ns_by_stream = BinaryStream(binary=binary_name_space)
        name_space = NameSpace(ns_by_stream)

        # Get XML-Object
        binary_xml = self.file.binary_xml()
        xml_by_stream = BinaryStream(binary=binary_xml)
        self.xml = XMLObject(xml_by_stream, name_space).todict()

    def _rate(self):
        rate = None
        for wavetrack in self.xml['project']['wavetrack']:
            if rate is None:
                rate = wavetrack['rate']
            else:
                if wavetrack['rate'] != rate:
                    raise ValueError("Different Samplerates!")
        
        return int(rate)
    
    def _sampleformt(self, format_id):
        if format_id == 262159:
            return '<f4'
        else:
            raise ValueError('Unknown sample format!')
    
    def export_audio(self, file):
        rate = self._rate()
        wavetracks = []
        for channel in self.xml['project']['wavetrack']:
            waveblocks = []
            sampleformat = self._sampleformt(channel['sampleformat'])
            for waveblock in channel['waveclip']['sequence']['waveblock']:
                binary_block = self.file.binary_sammpleblock(waveblock['blockid'])
                waveblocks.append(np.frombuffer(binary_block, dtype=sampleformat))

            wavetracks.append(np.concatenate(waveblocks))
        audio = np.stack(wavetracks, axis=1)

        sf.write(file, audio, rate)
        return
    
    def export_label(self, file):
        with open(file, 'w') as f:
            for label in self.xml['project']['labeltrack']['label']:
                f.write(f"{label['t']:.8f}\t{label['t1']:.8f}\t{label['title']}\n")
        return

if __name__ == "__main__":
    path = "audacity.aup3"

    converter = Converter(path)
    converter.export_audio('audio.wav')
    converter.export_label("label.txt")