from dotenv import load_dotenv
import os
from azure.core.credentials import AzureKeyCredential
from azure.ai.language.questionanswering import QuestionAnsweringClient
import azure.cognitiveservices.speech as speech_sdk
import speech_recognition as sr


def main():
    #getting all credentials for our program
    load_dotenv()
    #for speech
    cog_key = os.getenv('COG_SERVICE_KEY')
    cog_region = os.getenv('COG_SERVICE_REGION')
    #for qna
    endpoint = os.getenv('lang_endpoint')
    credential = AzureKeyCredential(os.getenv('lang_credential'))
    knowledge_base_project = "normaltalk"
    deployment = "production"

    
    speech_config = speech_sdk.SpeechConfig(cog_key, cog_region)
    speech_config.speech_synthesis_voice_name = "en-GB-RyanNeural"
    global speech_synthesizer
    speech_synthesizer = speech_sdk.SpeechSynthesizer(speech_config)

    introduction()
    while(True):
        user_voice=take_input()
        if user_voice == 'quit':
            print('Thank you.')
            break
        bot = QuestionAnsweringClient(endpoint,credential) #our brain to answer 
        with bot:
            question=user_voice
            output = bot.get_answers(
                question = question,
                project_name=knowledge_base_project,
                deployment_name=deployment
            )
        ans=output.answers[0].answer
        print(ans)
        speak = speech_synthesizer.speak_text_async(ans).get()
        if speak.reason != speech_sdk.ResultReason.SynthesizingAudioCompleted:
            print(speak.reason)


    

def take_input(): #function to listen to user
    r = sr.Recognizer()
    
    with sr.Microphone() as source: 
        print('Listening')
        r.pause_threshold = 1
        audio = r.listen(source)
    try:
        user_voice= r.recognize_google(audio, language = 'en-in')
        print(f'You said- {user_voice}\n')
    except Exception as e:
        print('Could not understand what you said, say again please')
        return "None"
    return user_voice

def introduction():
    speech_synthesizer.speak_text_async("Hey, I am your conversation freind, say Quit to exit.").get()
if __name__== '__main__':
    main()


