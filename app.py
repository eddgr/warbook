import collections
import csv
import datetime
import os
import sys

import boto3


def _check_file_exists(filename):
    """
    Check if file exists in directory.
    """
    return os.path.isfile(filename)


def _date_format():
    """
    Return date format string `YYYYMMDD`.
    """
    return '%Y%m%d'


def _update_csv_file(csv_filename, csv_headers, csv_dict):
    file_exists = _check_file_exists(csv_filename)
    with open(csv_filename, 'a') as file:
        writer = csv.DictWriter(file, fieldnames=csv_headers)
        # write headers only once
        if not file_exists:
            writer.writeheader()
        writer.writerow(csv_dict)


def add_entry(filename='rawbook.csv'):
    utcnow = datetime.datetime.utcnow()
    utc_datetime = utcnow.strftime(f'{_date_format()} - %H:%M:%S')
    # set Fridays as eow
    eow = (
        utcnow.date() + datetime.timedelta(days=4 - utcnow.weekday())
    ).strftime(_date_format())

    entry = input(f'New Entry [{utc_datetime}]: ')
    
    headers = ['eow','utc_datetime','entry']
    values = [eow, utc_datetime, entry]
    entry_dict = dict(zip(headers, values))
    print(entry_dict)

    _update_csv_file(filename, headers, entry_dict)


def _return_date_day(date):
    """
    Return date string of `YYYYMMDD - Day`.
    """
    date_only = date.split(' - ')[0]
    date_day = datetime.datetime.strptime(
        date_only, _date_format()).strftime('%A')
    return f'{date_only} - {date_day}'


def _generate_md_file(md_filename, md_dict):
    with open(md_filename, 'w') as md_file:
        for eow, date_entries in sorted(md_dict.items(), reverse=True):
            # Create eow header
            md_file.write(f'# {eow}\n')
            for day, entries in date_entries.items():
                # Create day sub header
                md_file.write(f'### {day}\n')
                for entry in entries:
                    # List entries
                    md_file.write(f'* {entry}\n')


def to_markdown(filename='rawbook.csv', markdown_filename='warbook.md'):
    if not _check_file_exists(filename):
        raise FileNotFoundError

    markdown_dict = collections.defaultdict(
        lambda: collections.defaultdict(list))
    with open(filename, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            date = _return_date_day(row['utc_datetime'])
            markdown_dict[row['eow']][date].append(row['entry'])

    _generate_md_file(markdown_filename, markdown_dict)


def _envget(key, default=None):
    """
    Helper function to retrieve environment variable.
    """
    value = os.environ.get(key, default)
    if value == 'True':
        return True
    if value == 'False':
        return False
    return value


def sync_s3(filename):
    if not _check_file_exists(filename):
        raise FileNotFoundError

    bucket_name = _envget('S3_BUCKET')

    s3 = boto3.resource(
        's3',
        aws_access_key_id=_envget('S3_ACCESS_KEY_ID'),
        aws_secret_access_key=_envget('S3_ACCESS_SECRET_KEY'))

    my_bucket = s3.Bucket(bucket_name)

    my_bucket.Object(filename).put(Body=open(filename, 'rb'))


if __name__ == '__main__':
    func_name = sys.argv[1]

    if func_name == 'sync_s3':
        filename_arg = sys.argv[2]
        globals()[func_name](filename_arg)
    else:
        globals()[func_name]()
