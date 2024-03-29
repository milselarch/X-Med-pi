#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import base64
import datetime
import hashlib
import hmac
import json

import requests

# Key derivation functions
# http://docs.aws.amazon.com/general/latest/gr/signature-v4-examples.html#signature-v4-examples-python
def sign(key, msg):
    return hmac.new(key, msg.encode('utf-8'), hashlib.sha256).digest()


def getSignatureKey(key, date_stamp, regionName, serviceName):
    kDate = sign(('AWS4' + key).encode('utf-8'), date_stamp)
    kRegion = sign(kDate, regionName)
    kService = sign(kRegion, serviceName)
    kSigning = sign(kService, 'aws4_request')
    return kSigning


if __name__ == '__main__':
    # Read credentials from the environment
    # access_key = os.environ.get('AKIAI4WW3DVEP4W2HLXA')
    # secret_key = os.environ.get('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')
    access_key = os.environ.get('AWS_ACCESS_KEY_ID')
    secret_key = os.environ.get('AWS_SECRET_ACCESS_KEY')

    # Uncomment this line if you use temporary credentials via STS or similar
    #token = os.environ.get('AWS_SESSION_TOKEN')

    if access_key is None or secret_key is None:
        print('No access key is available.')
        sys.exit()

    # This code shows the v4 request signing process as shown in
    # http://docs.aws.amazon.com/general/latest/gr/sigv4-signed-request-examples.html

    host = 'rekognition.us-east-1.amazonaws.com'
    endpoint = 'https://rekognition.us-east-1.amazonaws.com'
    service = 'rekognition'

    # Currently, all Rekognition actions require POST requests
    method = 'POST'

    region = 'us-east-1'

    # This defines the service target and sub-service you want to hit
    # In this case you want to use 'CompareFaces'
    amz_target = 'RekognitionService.CompareFaces'



    # Amazon content type - Rekognition expects 1.1 x-amz-json
    content_type = 'application/x-amz-json-1.1'

    # Create a date for headers and the credential string
    now = datetime.datetime.utcnow()
    amz_date = now.strftime('%Y%m%dT%H%M%SZ')
    date_stamp = now.strftime('%Y%m%d') # Date w/o time, used in credential scope

    # Canonical request information
    canonical_uri = '/'
    canonical_querystring = ''
    canonical_headers = 'content-type:' + content_type + '\n' + 'host:' + host + '\n' + 'x-amz-date:' + amz_date + '\n' + 'x-amz-target:' + amz_target + '\n'

    # list of signed headers
    signed_headers = 'content-type;host;x-amz-date;x-amz-target'

    # Our source image: http://i.imgur.com/OK8aDRq.jpg
    with open('source.jpg', 'rb') as source_image:
        source_bytes = base64.b64encode(source_image.read())

    # Our target image: http://i.imgur.com/Xchqm1r.jpg
    with open('target.jpg', 'rb') as target_image:
        target_bytes = base64.b64encode(target_image.read())

    # here we build the dictionary for our request data
    # that we will convert to JSON
    request_dict = {
            'SimilarityThreshold': 75.0,
            'SourceImage': {
                'Bytes': source_bytes
            },
            'TargetImage': {
                'Bytes': target_bytes
            }
    }

    # Convert our dict to a JSON string as it will be used as our payload
    request_parameters = json.dumps(request_dict)

    # Generate a hash of our payload for verification by Rekognition
    payload_hash = hashlib.sha256(request_parameters).hexdigest()

    # All of this is 
    canonical_request = method + '\n' + canonical_uri + '\n' + canonical_querystring + '\n' + canonical_headers + '\n' + signed_headers + '\n' + payload_hash

    algorithm = 'AWS4-HMAC-SHA256'
    credential_scope = date_stamp + '/' + region + '/' + service + '/' + 'aws4_request'
    string_to_sign = algorithm + '\n' +  amz_date + '\n' +  credential_scope + '\n' +  hashlib.sha256(canonical_request).hexdigest()

    signing_key = getSignatureKey(secret_key, date_stamp, region, service)
    signature = hmac.new(signing_key, (string_to_sign).encode('utf-8'), hashlib.sha256).hexdigest()

    authorization_header = algorithm + ' ' + 'Credential=' + access_key + '/' + credential_scope + ', ' +  'SignedHeaders=' + signed_headers + ', ' + 'Signature=' + signature

    headers = { 'Content-Type': content_type,
            'X-Amz-Date': amz_date,
            'X-Amz-Target': amz_target,

            # uncomment this if you uncommented the 'token' line earlier
            #'X-Amz-Security-Token': token,
            'Authorization': authorization_header}

    r = requests.post(endpoint, data=request_parameters, headers=headers)

    # Let's format the JSON string returned from the API for better output
    formatted_text = json.dumps(json.loads(r.text), indent=4, sort_keys=True)

    print('Response code: {}\n'.format(r.status_code))
    print('Response body:\n{}'.format(formatted_text))
