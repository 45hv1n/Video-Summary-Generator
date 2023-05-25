from api_secret import API_SECRET_KEY
import requests
import time

upload_endpoint = 'https://api.assemblyai.com/v2/upload'
transcript_endpoint = 'https://api.assemblyai.com/v2/transcript'

#Upload Header
headers_auth_only = {'authorization': API_SECRET_KEY}

#Transcript Header
headers = {
    "authorization": API_SECRET_KEY,
    "content-type": "application/json"
}

CHUNK_SIZE = 5242880  # 5MB


def upload(filename):
    def read_file(filename):
        with open(filename, 'rb') as f:
            while True:
                data = f.read(CHUNK_SIZE)
                if not data:
                    break
                yield data

    upload_response = requests.post(upload_endpoint, headers=headers_auth_only, data=read_file(filename))
    return upload_response.json()['upload_url']

#print(upload("/home/arvin/Desktop/p3r50n47/VTT/test1.mp3"))


def transcribe(audio_url):
    transcript_request = {
        "audio_url" : audio_url,
        "summarization" : True,
        "summary_model" : "informative",
        "summary_type" : "bullets"
        
    }

    transcript_response = requests.post(transcript_endpoint, json=transcript_request, headers=headers)
    return transcript_response.json()['id']

        
def poll(transcript_id):
    polling_endpoint = transcript_endpoint + '/' + transcript_id
    polling_response = requests.get(polling_endpoint, headers=headers)
    return polling_response.json()


def get_transcription_result_url(url):
    transcribe_id = transcribe(url)
    while True:
        data = poll(transcribe_id)
        if data['status'] == 'completed':
            return data, None
        elif data['status'] == 'error':
            return data, data['error']
            
        print("waiting for 30 seconds")
        time.sleep(30)

response = get_transcription_result_url(upload("/home/arvin/Desktop/p3r50n47/VTT/test1.mp3"))

#print(response[0]["text"])


