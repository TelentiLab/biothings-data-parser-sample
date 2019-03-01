import logging
import os

FILE_NOT_FOUND_ERROR = 'Cannot find input file: {}'   # error message constant

# configure logger
logging.basicConfig(format='%(asctime)s %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s', level=logging.INFO)
_logger = logging.getLogger('biothings_parser')

# change following parameters accordingly
SOURCE_NAME = 'my_data_source'   # source name that appears in the api response
FILENAME = 'sample_data.tsv'   # name of the file to read
DELIMITER = '\t'    # the delimiter that separates each field


def _inspect_file(filename: str) -> int:
    with open(filename) as f:
        for i, l in enumerate(f):
            pass
    return i + 1


def load_data(data_folder: str):
    """
    Load data from a specified file path. Parse each line into a dictionary according to the schema.
    Then process each dict by normalizing data format, remove null fields (optional).
    Append each dict into final result using its id.

    :param data_folder: the path(folder) where the data file is stored
    :return: a generator that yields data.
    """
    input_file = os.path.join(data_folder, FILENAME)
    # raise an error if file not found
    if not os.path.exists(input_file):
        _logger.error(FILE_NOT_FOUND_ERROR.format(input_file))
        raise FileExistsError(FILE_NOT_FOUND_ERROR.format(input_file))

    file_lines = _inspect_file(input_file)  # get total lines so that we can indicate progress in next step

    with open(input_file, 'r') as file:
        _logger.info(f'start reading file: {FILENAME}')
        count = 0
        skipped = []
        for line in file:
            count += 1
            _logger.info(f'reading line {count} ({(count / file_lines * 100):.2f}%)')  # format to use 2 decimals

            if line.startswith('#') or line.strip() == '':
                skipped.append(line)
                continue  # skip commented/empty lines

            try:
                chrom, start, end, percentile = line.strip().split(DELIMITER)   # unpack according to schema
            except ValueError:
                _logger.error(f'failed to unpack line {count}: {line}')
                _logger.error(f'got: {line.strip().split(DELIMITER)}')
                skipped.append(line)
                continue  # skip error line

            try:    # parse each field if necessary (format, enforce datatype etc.)
                chrom = chrom.replace('chr', '')
                start = int(start)
                end = int(end)
                percentile = float(percentile)
            except ValueError as e:
                _logger.error(f'failed to cast type for line {count}: {e}')
                skipped.append(line)
                continue  # skip error line

            _id = f'chr{chrom}:g.{start}_{end}'  # define id

            variant = {
                'chrom': chrom,
                'start': start,
                'end': end,
                'percentile': percentile,
            }

            yield {  # commit an entry by yielding
                "_id": _id,
                SOURCE_NAME: variant
            }
        _logger.info(f'parse completed, {len(skipped)}/{file_lines} lines skipped.')
        for x in skipped:
            _logger.info(f'skipped line: {x.strip()}')
