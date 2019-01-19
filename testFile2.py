from google.cloud import speech_v1p1beta1 as speech
client = speech.SpeechClient()

speech_file = 'uofthacks/resources/record 1.wav'

with open(speech_file, 'rb') as audio_file:
    content = audio_file.read()

audio = speech.types.RecognitionAudio(content=content)

config = speech.types.RecognitionConfig(
    encoding=speech.enums.RecognitionConfig.AudioEncoding.LINEAR16,
    language_code='en-US',
    enable_automatic_punctuation=True,
    enable_speaker_diarization=True,
    diarization_speaker_count=2,
    audio_channel_count=2)

response = client.recognize(config, audio)

# print('full results', response.results)
#print(u'Speaker Tag: {}'.format(result.speaker_tag))
#print('type of result', type(response.results))

#print ('response test', response)

resultText = ""

for i, result in enumerate(response.results):
    alternative = result.alternatives[0]
    #print('-' * 20)
    #print('First alternative of result {}'.format(i))
    #print(u'Transcript: {}'.format(alternative.transcript))
    #print("transcripttttt-------------->", alternative.transcript)
    #print("type---------->", type(alternative.transcript))
    resultText += alternative.transcript
    resultText += " \n"
    #print(u'Channel Tag: {}'.format(result.channel_tag))
    #print(u'Speaker Tag: {}'.format(result.speaker_tag))

print("Final transcript:", resultText)
# for i, result in enumerate(response.results):
#     alternative = result.alternatives[0]
#     print('-' * 20)
#     print('First alternative of result {}'.format(i))
#     print(u'Transcript: {}'.format(alternative.transcript))
#     print(u'Channel Tag: {}'.format(result.channel_tag))
#     #print(u'Speaker Tag: {}'.format(result.speaker_tag))