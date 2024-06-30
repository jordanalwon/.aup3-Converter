# .aup3-Converter
*.aup3-Converter* extracts the data of an Audacity project file (.aup3) and makes it available for further processing or saves the data in more accessible file formats.

.aup3-Converter is MIT licensed
(c) 2024, Jordan Alwon

## Installation
*.aup3-Converter* has following dependencies:
- Numpy
- Soundfile
- tqdm

## Export Data
```python
from convert import Converter
converter = Converter(path)
converter.export_audio('export.wav')
converter.export_label("export.txt")
```

## Roadmap to v1.0
- [ ] Add Testframework
- [ ] Integrate Tests to Github CI
- [ ] Complete Docstring
- [ ] Generate Documentation from docstring
- [ ] Create C/C++ file reader to speed up the process