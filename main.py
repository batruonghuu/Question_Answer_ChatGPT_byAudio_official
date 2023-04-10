import gradio as gr
import openai
# import pyttsx3
import speech_recognition as sr
# import numpy as np
# from transformers import pipeline
# import tensorflow

# p = pipeline("automatic-speech-recognition")
recog = sr.Recognizer()
openai.api_key = open('key.txt','r').read().strip('\n')
messages_history = []

# voice_assistant = pyttsx3.init()
# voice = voice_assistant.getProperty('voices')
# voice_assistant.setProperty('voice',voice[1].id)

# def speak(audio):
#     voice_assistant.say(audio)
#     voice_assistant.runAndWait()

# def command():
#     c = sr.Recognizer()
#     with sr.Microphone() as source:
#         c.pause_threshold = 2
#         audio = c.listen(source)
#     try:
#         query = c.recognize_google(audio,language='en')
#         return query
#     except sr.UnknownValueError:
#         print("Please repeat or typing the command")

def itself(audio):
    with sr.AudioFile(audio) as source:
        audio_data = recog.record(source)
        text = recog.recognize_google(audio_data=audio_data, language='en-US')
    return text

# def transcribe(audio):
#     # text = p(audio)["text"]
#     # return text
#     recog = sr.Recognizer()
#     audio_np = audio[0]
#     # sample_rate = audio[1]
#     # sample_width = audio.dtype.itemsize
#     audio_to_byte = sr.AudioData((audio[0],audio[1]),sample_rate=16000,sample_width=2)
#
#     try:
#         transcript = recog.recognize_google(audio_to_byte)
#     except sr.UnknownValueError:
#         transcript = "Unable to recognize speech"
#     except sr.RequestError as e:
#         transcript = "Error Network"
#     return transcript
# print('your command')
# text = command()
# print(text)
# # while True:
# # print(sr.Microphone.list_microphone_names())
#     # print('what your command')
#     # query = command().lower()
#     # print(query)

def predict(inp):
    messages_history.append({'role':'user','content':inp})
    completion = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=messages_history,
    #     truyen messages_history de giup kha nang tu hoc cua chatGPT bot
    )
    reply_content = completion.choices[0].message.content
    # print(reply_content)
    messages_history.append({'role':'assistant','content':reply_content})
    response = [(messages_history[i]['content'],messages_history[i+1]['content']) for i in range(0,len(messages_history),2)]
    return response
# for i in range(2):
#     user_input = input(">:")
#     print(user_input)
#     print(chat(user_input))
# def transcribe_action(input_audio):
#     output = transcribe(input_audio)
#     txt.submit(predict, txt, chatbot)
#     txt.submit(lambda: "", None, txt)
#     txt.submit(None, None, txt, _js="() => {''}")
#     return output

with gr.Blocks() as demo:
    chatbot = gr.Chatbot()
    with gr.Tab("Text"):
        txt = gr.Textbox(show_label=False,placeholder='Type your message here').style(container=False)
        txt.submit(predict,txt,chatbot)
        txt.submit(lambda: "",None,txt)
        txt.submit(None,None,txt,_js="() => {''}")
    with gr.Tab("Speech_to_Text"):
        with gr.Row().style(mobile_collapse=False, equal_height=True):
            gr_audio = gr.Audio(
                label="Input Audio",
                show_label=False,
                source="microphone",
                type="filepath"
            )
            btn = gr.Button("Transcribe")

        # button = gr.Button(value = 'Click to Speak (by English or Vietnamese)')
        # gr_audio = gr.Audio(source="microphone", type="filepath")
        # gr_audio = gr.Microphone()
        outputs_audio = gr.Textbox()
        btn.click(itself,inputs=gr_audio,outputs=outputs_audio)
        submit_button = gr.Button("Submit your message")
        submit_button.click(predict,inputs=outputs_audio,outputs=chatbot)
        submit_button.click(lambda: "",inputs=None,outputs=outputs_audio)

        # gr.Interface(transcribe,inputs=gr_audio,outputs=outputs_audio)
        # print(gr_audio.value)

        # print(gr_audio)
        # submit_button.click(fn=transcribe,inputs=gr_audio,outputs=outputs_audio)
            # txt.submit(predict,txt,chatbot)
            # txt.submit(lambda: "",None,txt)
            # txt.submit(None,None,txt,_js="() => {''}")


#
demo.launch(share=True)
# print(gr_audio.value)