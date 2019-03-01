# Introduction

This is a sample data parser for [Biothings Studio](http://docs.biothings.io/en/latest/doc/studio.html). This repo does not contain any information regarding [Biothings Studio](http://docs.biothings.io/en/latest/doc/studio.html), please refer to the original link if you need more information on Biothings Studio. It is highly recommended that you go through the [tutorials](http://docs.biothings.io/en/latest/doc/studio_tutorial.html) and [developer guide](http://docs.biothings.io/en/latest/doc/studio_guide.html) in Biothings Studio page first.

# Usage

## Installation

This Python project uses [**pipenv**](https://pipenv.readthedocs.io/en/latest/) to manage virtual environment.

To install **pipenv**:

```bash
pip isntall pipenv
```

To create project virtual environment, along with the dependencies:

```bash
pipenv isntall
``` 

Hint: make sure you have Python `3.6` installed.

Once you have set up the virtual environment, you are ready to go. You can tailor the code to your need. Refer to the next section on how to do that.

# Explanation

## High Level Ideas
 
We defined a method, `load_data()` in `parser.py`, specified in `manifest.json` file to be the parser for **Biothings Studio**. `parser.load_data()` returns a generator that yields one record at a time, which will be used by **Biothings Studio**.

## Details

These are the files you need to walk through if you want to customize your own parser.

### `manifest.json`

Defines data download (dumper) and parsing (uploader) logic as well as metadata. More details covered in **Biothings Studio** tutorials.

### `parser.py`

Below is the workflow. Customize it to your demand.

1. Define data file name, delimiter and source name:

    - `FILENAME`: filename does not include the path.
    - `DELIMITER`: what you used to separate fields in the data file. For example, `,` in a `.csv` file or `\t` in a `.tsv` file.
    - `SOURCE_NAME`: the key name to be shown in the API response for your data. For example:
    
    ```
    {
        _id: ...,
        my_data_source: {
            ...,    # some data
        }
    }
    ```

1. Check if file exists in path.

1. Inspect file to get the total number of lines. (optional but recommended for logging purpose so that we can indicate progress in the following steps)

1. Read file:
    - Skip commented lines and empty lines
    - Split line according to schema. Skip the line when split fails, record to `skipped` list.
    - Format and enforce data type for each fields. Skip the line when cast fails, record to `skipped` list.
    - Construct an entry and yield it.
    - Output all skipped lines (`skipped` list) to log after finished.

### sample.tsv

A sample file provided for testing purpose.


