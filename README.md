# Besepa SDK 

**ALPHA STAGE, dont use in production**

The Besepa SDK provides Python APIs to create, process and manage SEPA direct debits. The [Besepa APIs](http://docs.besepaen.apiary.io/) ara fully supported by the SDK.


## Installation

Install using `pip`:
```sh
pip install besepasdk
```

## Configuration

Register a account and get your api_key at [Besepa Portal](http://www.besepa.com/).

```python
import besepasdk
besepasdk.configure({
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
import besepasdk
my_api = besepasdk.Api({
  'mode': 'sandbox',
  'api_key': '...'})

payment = besepasdk.Debit({...}, api=my_api)
```

## Development

To work on the Besepa SDK codebase, you'll want to clone the repository,
and create a Python virtualenv with the project requirements installed:
```bash
$ git clone git@github.com:txerpa/besepasdk.git
$ cd besepasdk
$ ./scripts/setup
```
To run the continuous integration tests and code linting:
```bash
$ ./scripts/test
$ ./scripts/lint
```
