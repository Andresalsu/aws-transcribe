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

def makeTrans(job_uri):

    #Se inicia el servicio de AWS con Boto3 para el almacenamiento del audio en un bucket de S3
    S3 = boto3.client('s3')
    job_name = "jobname-"+str(datetime.datetime.now()).replace(' ','_').replace(':','-')
    print(job_name)

    #Se almacena el archivo en el bucket
    SOURCE_FILENAME = job_uri.filename
    BUCKET_NAME = 'speech-to-text-edi'
    S3.upload_file(SOURCE_FILENAME, BUCKET_NAME, SOURCE_FILENAME)

    #Se inicia el servicio de AWS con Boto3 para la transcripcion del audio
    transcribe = boto3.client('transcribe')
    #Se referencia el nombre del Job para la transcripcion, la ubicacion del audio, el tipo de archivo y el lenguaje 
    transcribe.start_transcription_job(
        TranscriptionJobName=job_name,
        Media={'MediaFileUri': "s3://speech-to-text-edi/"+str(os.path.basename(job_uri.filename))},
        MediaFormat='wav',
        LanguageCode='es-ES'

    )

    #Mientras se transcribe el audio se espera un tiempo para la transcripcion
    while True:
        status = transcribe.get_transcription_job(TranscriptionJobName=job_name)
        if status['TranscriptionJob']['TranscriptionJobStatus'] in ['COMPLETED', 'FAILED']:
            break
        print("Not ready yet...")
        time.sleep(5)

    #Finalmente, se recibe una URL con un JSON que contiene el resultado. Del JSON se extrae el texto detectado y se retorna
    url = status['TranscriptionJob']['Transcript']['TranscriptFileUri']
    req = urllib.request.Request(url)
    gcontext = ssl.SSLContext()
    response = urllib.request.urlopen(req,context=gcontext)
    data = json.loads(response.read())
    return data['results']['transcripts'][0]['transcript']
