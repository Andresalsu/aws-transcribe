# COPYRIGHT:
# 
# Copyright 2018-2019 Amazon.com, Inc. or its affiliates. All Rights Reserved.
# 
# Licensed under the Apache License, Version 2.0 (the "License").
# You may not use this file except in compliance with the License.
# A copy of the License is located at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# or in the "license" file accompanying this file. This file is distributed
# on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either
# express or implied. See the License for the specific language governing
# permissions and limitations under the License.
# 
from __future__ import print_function

import time, datetime
import boto3
import json
import urllib
import ssl
import os

job_name = "jobname"+str(datetime.datetime.now()).replace(' ','_').replace(':','-')

def makeTrans(job_uri):

    S3 = boto3.client('s3')

    SOURCE_FILENAME = job_uri.filename+'.wav'
    BUCKET_NAME = 'speech-to-text-edi'
    S3.upload_file(SOURCE_FILENAME, BUCKET_NAME, SOURCE_FILENAME)

    transcribe = boto3.client('transcribe')
    transcribe.start_transcription_job(
        TranscriptionJobName=job_name,
        Media={'MediaFileUri': "s3://speech-to-text-edi/"+str(os.path.basename(job_uri.filename)+'.wav')},
        MediaFormat='wav',
        LanguageCode='es-ES'

    )

    while True:
        status = transcribe.get_transcription_job(TranscriptionJobName=job_name)
        if status['TranscriptionJob']['TranscriptionJobStatus'] in ['COMPLETED', 'FAILED']:
            break
        print("Not ready yet...")
        time.sleep(5)

    url = status['TranscriptionJob']['Transcript']['TranscriptFileUri']
    req = urllib.request.Request(url)
    gcontext = ssl.SSLContext()
    response = urllib.request.urlopen(req,context=gcontext)
    data = json.loads(response.read())
    return data['results']['transcripts'][0]['transcript']
