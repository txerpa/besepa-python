# Besepa Python 
[![Build Status](https://travis-ci.org/txerpa/besepa-python.svg?branch=master)](https://travis-ci.org/txerpa/besepa-python) [![codecov](https://codecov.io/gh/txerpa/besepa-python/branch/master/graph/badge.svg)](https://codecov.io/gh/txerpa/besepa-python) [![Scrutinizer Code Quality](https://scrutinizer-ci.com/g/txerpa/besepa-python/badges/quality-score.png?b=master)](https://scrutinizer-ci.com/g/txerpa/besepa-python/?branch=master)

**ALPHA STAGE, dont use in production**

The Besepa Python provides simple python wrapper to Besepa.com's API. The [Besepa APIs](http://docs.besepaen.apiary.io/) ara fully supported by the SDK.


## Installation

Install using `pip`:
```sh
pip install besepa
```

## Configuration

Register a account and get your api_key at [Besepa Portal](http://www.besepa.com/).

```python
import besepa
besepa.configure({
  "mode": "sandbox", # sandbox or live
  "api_key": "EBWKjlELKMYqRNQ6sYvFo64FtaRLRR5BdHEESmha49TM" })
```

Configure through environment variables:
```sh
export BESEPA_MODE=sandbox   # sandbox or live
export BESEPA_API_KEY=EBWKjlELKMYqRNQ6sYvFo64FtaRLRR5BdHEESmha49TM
```

Configure through a non-global API object
```python
import besepa
my_api = besepa.Api({
  'mode': 'sandbox',
  'api_key': '...'})

payment = besepa.Debit({...}, api=my_api)
```

## Development

To work on the Besepa SDK codebase, you'll want to clone the repository,
and create a Python virtualenv with the project requirements installed:
```bash
$ git clone git@github.com:txerpa/besepa.git
$ cd besepa
$ ./scripts/setup
```
To run the continuous integration tests and code linting:
```bash
$ ./scripts/test
$ ./scripts/lint
```
