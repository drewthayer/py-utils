import boto3
from s3fs.core import S3FileSystem
import pandas as pd
from io import StringIO
import logging
import pdb

logging.basicConfig(format='[%(asctime)s] %(funcName)s %(lineno)d - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',level=logging.INFO)
logger = logging.getLogger(__name__)

class S3FileHandler():
    """ Utility for pandas <> s3.
    """

    def __init__(self, aws_profile=None):
        #self.aws_profile = aws_profile
        self.s3 = S3FileSystem(anon=False, profile=aws_profile)

    def split_s3_path(self, path):
        """ Split bucket name and key from an s3 path
        """
        if path.startswith('s3://'):
            path_ = path.split('//')[1]
            bucket = path_.split('/')[0]
            key = '/'.join(path_.split('/')[1:])
            return bucket, key
        else:
            logger.info('path does not start with s3://')
            return None

    def load_df_from_s3(self, s3_path, **kwargs):
        try:
            df = pd.read_csv(self.s3.open(s3_path), **kwargs)
            logger.info('df loaded from {}'.format(s3_path))
            return df
        except Exception as e:
            logger.info(e)

    def write_df_to_s3(self, df, s3_path, **kwargs):
        try:
            with self.s3.open(s3_path, 'w') as f:
                df.to_csv(f, **kwargs)
                logger.info('df written to {}'.format(s3_path))
        except Exception as e:
            logger.info(e)

def get_s3_resource(profile_name):
    session = boto3.Session(profile_name=profile_name)

    return session.resource('s3')


def start_s3_session(profile_name, region_name='us-west-2', log=True, return_region=False): # from my utils library
    """ create a session with a user with full S3 credentials
    e.g. dt-user
    param:
    profile_name    an AWS profile with S3 read/write permission
    return:
    s3              s3 session resource
    option to return the aws region for the session
    """
    session = boto3.Session(profile_name=profile_name, region_name=region_name)
    region = session.region_name
    if log:
        logger.info(f's3 session started, profile {profile_name}, region: {session.region_name}')

    # create a resource (high-level object) and create a bucket
    s3_resource = session.resource('s3')

    if return_region:
        return s3_resource, region
    else:
        return s3_resource


def split_s3_path(path):
    """ Split bucket name and key from an s3 path
    """
    if path.startswith('s3://'):
        path_ = path.split('//')[1]
        bucket = path_.split('/')[0]
        key = '/'.join(path_.split('/')[1:])
        return bucket, key
    else:
        return None


def upload_file(s3_resource, bucket_name, file, key_name, log=True):
    """ Upload a file to an s3 bucket with an s3 resource.
    param:
    s3              an s3 session resource
    bucket_name     str, a valid s3 bucket
    file            str, path to file on local
    key_name        str, filepath on s3
    """
    bucket = s3_resource.Bucket(bucket_name)
    bucket.upload_file(file, key_name)
    if log:
        logger.info(f'{file} uploaded to {bucket_name}/{key_name}')

def download_fileobj(s3_resource, bucket_name, key, log=True):
    pass

def load_csv_to_df(s3_resource, bucket_name, key, log=True):
    obj = s3_resource.meta.client.get_object(Bucket=bucket_name, Key=key)
    lines = obj['Body'].read().decode('utf-8').split()
    df = pd.read_csv(StringIO('\n'.join(lines)))

    return df

def load_csv_from_s3(s3_path, aws_profile=None):
    try:
        s3 = S3FileSystem(anon=False, profile=aws_profile)
        df = pd.read_csv(s3.open(s3_path))
        return df
    except Exception as e:
        logger.info(e)

def write_df_to_s3(df, bucket, key, aws_profile=None):
    try:
        s3 = S3FileSystem(anon=False, profile=aws_profile)
        with s3.open(bucket + '/' + key, 'w') as f:
            df.to_csv(f)
    except Exception as e:
        logger.info(e)
