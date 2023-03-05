import torch
from flask import Flask, jsonify, request
import requests
import time
import openai
import numpy as np
import json
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from string import punctuation
from collections import defaultdict
from heapq import nlargest
from transformers import T5ForConditionalGeneration, T5Tokenizer
import torch
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
from nltk.tokenize import sent_tokenize, word_tokenize
# import cv2
# import pytesseract
from collections import Counter
API_URL = "https://api-inference.huggingface.co/models/Hridayesh7/autotrain-summasense-3584196302"



class SummarizerModel:
    
    def title(text):
    # Load pre-trained T5 model
        print(text)
        nltk.download('omw-1.4')
        nltk.download('stopwords')
        nltk.download('wordnet')
        nltk.download('punkt')
        try:
            print("hi")
            # Load pre-trained T5 model
            sentences = sent_tokenize(text)
            words = word_tokenize(text.lower())
            # Remove stopwords and punctuation
            stepwords = set(stopwords.words('english') + list(punctuation))
            filtered_words = [word for word in words if word not in stepwords]
            # Build a dictionary of word frequencies
            word_freq = defaultdict(int)
            for word in filtered_words:
                word_freq[word] += 1
            # Normalize the word frequencies
            max_freq = max(word_freq.values())
            for word in word_freq:
                word_freq[word] = word_freq[word]/max_freq
            # Build a dictionary of sentence scores based on word frequencies
            sentence_scores = defaultdict(int)
            for i, sentence in enumerate(sentences):
                for word in word_tokenize(sentence.lower()):
                    if word in word_freq:
                        sentence_scores[i] += word_freq[word]
            # Get the top N sentences based on their scores
            num_sentences = 1
            top_sentences = nlargest(num_sentences, sentence_scores, key=sentence_scores.get)
            # Generate the summary or title from the top sentences
            title = ' '.join([sentences[i] for i in sorted(top_sentences)])
            print(title)
            return title
        except Exception as e:
            print(e)
            return "error"
        
    def t5_summarizer(text,stop_words,top):
        try:
            while True:
                loading_response = requests.get(API_URL)
                if loading_response.json()["model_status"]["ready"]:
                    break
                time.sleep(loading_response.json()["model_status"]["estimated_time"])
            headers = {"Authorization": "Bearer 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"}
            data = {
                "inputs": f"summarize: {text}",
                 "parameters": {
                    "do_sample": True,
                    "max_length": stop_words,
                    "top_k": top,
                    "num_return_sequences": 1,
                    },
                }
            response = requests.post(API_URL, headers=headers, json=data)
            print("Yup",response.json())
            summary = response.json()[0]['summary_text']
            return jsonify({"summary": summary}),200
        except Exception as e:
            print("K",e)
            return "error"

    # def gpt(text):
    #     try:
    #         openai.api_key = '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'
    #         model_engine = "text-davinci-002"
    #         prompt_prefix = "Please summarize the following text:"
    #         temperature = 0.7
    #         max_tokens = 200
    #         prompt = prompt_prefix + "\n" + text
    #         response = openai.Completion.create(engine=model_engine, prompt=prompt, temperature=temperature, max_tokens=max_tokens)
    #         summary = response.choices[0].text.strip()
    #         title=SummarizerModel.title(summary)
    #         return jsonify({"summary": summary,"title":title}),200
    #     except Exception as e:
    #         print("H",e)
    #         return "error"

        
    def lsa(text,num_sent):
        try:
            stop_words = set(stopwords.words('english'))
            wordnet_lemmatizer = WordNetLemmatizer()
            sentences = nltk.sent_tokenize(text)
            clean_sentences = []
            for sentence in sentences:
                words = nltk.word_tokenize(sentence)
                words = [word.lower() for word in words if word.isalnum() and word.lower() not in stop_words]
                words = [wordnet_lemmatizer.lemmatize(word) for word in words]
                clean_sentences.append(' '.join(words))
            vectorizer = TfidfVectorizer()
            vectorized_sentences = vectorizer.fit_transform(clean_sentences)
            lsa_model = TruncatedSVD(n_components=1)
            lsa_model.fit(vectorized_sentences)
            sentence_scores = vectorized_sentences.dot(lsa_model.components_.T)
            top_sentence_indices = np.argsort(sentence_scores.flatten())[::-1][:num_sent]
            top_sentence_indices.sort()
            summary = ' '.join([sentences[i] for i in top_sentence_indices])
            print(summary)
            return summary
        except Exception as e:
            print('l',e)
            return "error"


    def kl(text,n_sentences):
        print(n_sentences)
        try:
            stop_words = set(stopwords.words('english'))
            words = [word.lower() for word in word_tokenize(text) if word.isalnum() and word.lower() not in stop_words]
            word_freq = Counter(words)
            max_freq = max(word_freq.values())

            if max_freq > 0:
                for word in word_freq:
                    word_freq[word] /= max_freq

            summary = ''
            for i, sentence in enumerate(sent_tokenize(text)):
                sentence_words = [word.lower() for word in word_tokenize(sentence) if word.isalnum()]
                sentence_freq = Counter(sentence_words)
                # Compute KL divergence only for words in both the text and the sentence
                common_words = set(word_freq.keys()) & set(sentence_freq.keys())
                if common_words:
                    sentence_kl_div = sum(word_freq[i] * np.log2(word_freq[i] / sentence_freq[i]) for i in common_words)
                else:
                    sentence_kl_div = float('inf')
                if i < n_sentences:
                    summary += sentence + ' '
                else:
                    # Compute KL divergence for the whole text and the current sentence
                    common_words = set(word_freq.keys()) & set(sentence_freq.keys())
                    new_sentence_score = sum(word_freq[i] * np.log2(word_freq[i] / sentence_freq[i]) for i in common_words)
                    if new_sentence_score > sentence_kl_div:
                        summary = summary.replace(summary.split()[-1], sentence, 1)
            summary = summary.strip()
            return summary
        except Exception as e:
            print('kl',e)
            return 'error'
        
    # def video(vid):
    #     try:
    #         video = cv2.VideoCapture(vid)
    #         success, image = video.read()
    #         count = 0
    #         while success:
    #             cv2.imwrite(f"frame{count}.jpg", image)
    #             success, image = video.read()
    #             count += 1
    #         for i in range(count):
    #             image = cv2.imread(f"frame{i}.jpg")
    #             text = pytesseract.image_to_string(image)
    #             print(text)
    #             return text
    #     except Exception as e:
    #         print(e)
    #         return "error"



        
 

