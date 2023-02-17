import torch
from transformers import T5ForConditionalGeneration, T5Tokenizer
from transformers import BartForConditionalGeneration, BartTokenizer, BartConfig

bart_tokenizer=BartTokenizer.from_pretrained('facebook/bart-large-cnn')
bart_model=BartForConditionalGeneration.from_pretrained('facebook/bart-large-cnn')
t5_model = T5ForConditionalGeneration.from_pretrained('t5-large')
t5_tokenizer = T5Tokenizer.from_pretrained('t5-large')

class SummarizerModel:
    def t5_summarizer(text):
        try:
            text="summarize:"+text
            input_ids=t5_tokenizer.encode(text, return_tensors='pt', max_length=4000)
            summary_ids = t5_model.generate(input_ids,
                             early_stopping=True,
                             max_length=500,
                             min_length=100,
                             )
            summary_ids
            t5_summary = t5_tokenizer.decode(summary_ids[0])
            return t5_summary
        except Exception as e:
            print(e)
            return "error"
    def bart(text):
        try:
            inputs = bart_tokenizer.batch_encode_plus([text],return_tensors='pt')
            summary_ids = bart_model.generate(inputs['input_ids'], 
                             early_stopping=True,
                             max_length=500,
                             min_length=100,)
            bart_summary = bart_tokenizer.decode(summary_ids[0], skip_special_tokens=True)
            return bart_summary
        except Exception as e:
            print(e)
            return "error"