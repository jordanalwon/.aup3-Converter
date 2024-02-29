from .reader import SQLite3Reader
from .binary_stream import BinaryStream
from .name_space import NameSpace
from .xml_object import XMLObject
import numpy as np
import soundfile as sf
from tqdm import tqdm

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
    
    def _sampleformat(self, format_id):
        if format_id == 262159:
            return {'numpy':'<f4',
                    'soundfile': 'float32'}
        else:
            raise ValueError('Unknown sample format!')
    
    def _channels(self):
        return len(self.xml['project']['wavetrack'])
    
    def labels(self):
        return self.xml['project']['labeltrack']
    
    def export_audio(self, file):
        rate = self._rate()
        channels = self._channels()
        sampleformat = self._sampleformat(self.xml['project']['wavetrack'][0]['sampleformat'])
        blocks = len(self.xml['project']['wavetrack'][0]['waveclip']['sequence']['waveblock'])
        with sf.SoundFile(file, mode='w', samplerate=rate, channels=channels) as soundfile, tqdm(total=blocks*channels, desc="export audio") as pbar:
            for idx in range(blocks):
                c_data = []
                for c in range(channels):
                    block_id = self.xml['project']['wavetrack'][c]['waveclip']['sequence']['waveblock'][idx]['blockid']
                    binary_block = self.file.binary_sammpleblock(block_id)
                    c_data.append(np.frombuffer(binary_block, dtype=sampleformat['numpy']))
                    pbar.update()
                o_data = np.stack(c_data, axis=1)
                soundfile.buffer_write(o_data, dtype=sampleformat['soundfile'])
        return
    
    def export_label(self, file, sign_digits=6):
        with open(file, 'w') as f:
            for label in self.labels['label']:
                f.write(f"{label['t']:.{sign_digits}f}\t{label['t1']:.{sign_digits}f}\t{label['title']}\n")
        return

if __name__ == "__main__":
    path = "audacity.aup3"

    converter = Converter(path)
    converter.export_audio('audio.wav')
    converter.export_label("label.txt")