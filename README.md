# .aup3-Converter
*.aup3-Converter* extracts the data of an Audacity project file (.aup3) and makes it available for further processing or saves the data in more accessible file formats.

.aup3-Converter is MIT licensed
(c) 2024, Jordan Alwon

## Installation
*.aup3-Converter* depends on the Python packages NumPy and Soundfile.

## Export Data
```python
from convert import Converter
converter = Converter(path)
converter.export_audio('export.wav')
converter.export_label("export.txt")
```