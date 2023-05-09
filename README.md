# py-confparse
* parse cisco conf to table

## how to start project
```sh
$ cd py-confparse
$ python3 -m venv venv
$ . venv/bin/activate
$ pip3 install ciscoconfparse
$ python3 parse.py
```

## pip requirement
```sh
(venv) col@ub22201:~/projects/python/py-confparse$ python3 -m pip freeze
ciscoconfparse==1.7.18
deprecat==2.1.1
dnspython==2.3.0
et-xmlfile==1.1.0
loguru==0.6.0
numpy==1.24.3
openpyxl==3.1.2
pandas==2.0.1
passlib==1.7.4
python-dateutil==2.8.2
pytz==2023.3
six==1.16.0
toml==0.10.2
tzdata==2023.3
wrapt==1.15.0
(venv) col@ub22201:~/projects/python/py-confparse$ pip3 list
Package         Version
--------------- -------
ciscoconfparse  1.7.18
deprecat        2.1.1
dnspython       2.3.0
et-xmlfile      1.1.0
loguru          0.6.0
numpy           1.24.3
openpyxl        3.1.2
pandas          2.0.1
passlib         1.7.4
pip             22.0.2
python-dateutil 2.8.2
pytz            2023.3
setuptools      59.6.0
six             1.16.0
toml            0.10.2
tzdata          2023.3
wrapt           1.15.0
```

---
## Step1 - input and output folder 1parse
```python
def start_script(input_cfg):
    dir = os.path.dirname(__file__)
    indir = 'config'
    outdir = 'output'
    infile = input_cfg
    outfile = infile + '_out.csv'
    inf = os.path.join(dir, indir, infile)
    outf = os.path.join(dir, outdir, outfile)
```

## Step2 - start script
```sh
$ python3 1parse.py
$ python3 2merage.py
```

## reference
https://regex101.com/