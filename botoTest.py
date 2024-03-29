import pprint

import boto3

# Set this to whatever percentage of 'similarity'
# you'd want
SIMILARITY_THRESHOLD = 75.0

if __name__ == '__main__':
    client = boto3.client('rekognition')

    # Our source image: http://i.imgur.com/OK8aDRq.jpg
    with open('source.jpg', 'rb') as source_image:
        source_bytes = source_image.read()

    # Our target image: http://i.imgur.com/Xchqm1r.jpg
    with open('target.jpg', 'rb') as target_image:
        target_bytes = target_image.read()

    response = client.compare_faces(
                   SourceImage={ 'Bytes': source_bytes },
                   TargetImage={ 'Bytes': target_bytes },
                   SimilarityThreshold=SIMILARITY_THRESHOLD
    )

    print(response)
