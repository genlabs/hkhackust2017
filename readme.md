###HK HACKUST 2017

Small Utility program to translate coordinate data from Hong Kong Transport HK80 Coordinates data [link](http://theme.gov.hk/en/theme/psi/datasets/tsm_dataspec.pdf) to World Geodetic System WGS84 coordinates and use Google API to precalculate all the drawing point for Polyline in Google Map.

### Setup

```
$ mv config.ini.sample config.ini
```

edit the file and put your Google map API key 

### Run

```
$ python google-map-route.py
```

note: You can reduce running time by removing the sleep inside the code



