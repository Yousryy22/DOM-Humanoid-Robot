#!/usr/bin/env python3

###  integrating the voice recognition with chatbot and yolo image processing


# MAIN


import cv2
import numpy as np
import wave
import vosk
import sounddevice as sd
import queue
import pyttsx3
import random
import json
from transformers import AutoModelForCausalLM,AutoTokenizer
from lucas_test import ObjectDetector,  InvalidTarget

# vosk
model =vosk.Model("vosk-model-small-en-us-0.15")
recognizer = vosk.KaldiRecognizer(model,16000)
audio_queue = queue.Queue()

#huggingface  /  el model dialoGPT - medium
model_name ="microsoft/DialoGPT-medium"
tokenizer =AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

#el dataset elly f el json (gher el dataset bta3t el model)
with open("dataset.json","r") as f:
    dataset=json.load(f)

def get_random_response(user_input):

    user_input_lower = user_input.lower()
    words = user_input_lower.split()
    order = "".join(words[:1])    #awel kelma
    keyword = "".join(words[-1:])  #akher kelma

    if user_input_lower in dataset:
        responses = dataset[user_input_lower]
        return random.choice(responses) ,None  # json response
    elif order == "give" or order=="detect":
        return f"finding the {keyword} ", keyword  # hen bs bn3ml return ll keyword 3shan mhtagnha
    else:
        return chat_with_bot(user_input) ,None  #model response

def chat_with_bot(user_input):
    input_ids = tokenizer.encode(user_input + tokenizer.eos_token, return_tensors="pt")
    response_ids = model.generate(input_ids, max_length=100, pad_token_id=tokenizer.eos_token_id)
    response = tokenizer.decode(response_ids[:, input_ids.shape[-1]:][0], skip_special_tokens=True)
    return response

def callback(indata, frames, time, status):  #for mic
    audio_queue.put(bytes(indata))


with sd.RawInputStream(samplerate=16000, blocksize=8000, dtype="int16",
                       channels=1, callback=callback):
    print("speak now")

    while True:
        data = audio_queue.get()
        if recognizer.AcceptWaveform(data):
            result = recognizer.Result()
            print("user said:  ", result)

            #recognition
            output =(result[14:-3])   # result[14:-3] 3shan nakhod el string bs
            user_input = output

            if user_input.lower() =='exit':
                print("shutting down")
                break

            # RESPONSE
            response , keyword = get_random_response(user_input)
            word = response.split()
            word = "".join(word[:1])
            print(word)
            print(f"Robot: {response}")

            #tts output
            engine = pyttsx3.init()
            engine.say(response)
            engine.runAndWait()

            if word == "finding":   # check lw user made command
                try:
                    detector = ObjectDetector(target_object=keyword)
                    detector.start_video_capture()
                except InvalidTarget as e:  #error handling lw el object not found
                    print(e)
                    engine.say(f"cant find the {keyword}")
                    engine.runAndWait()
