from flask import jsonify, request
from app import app
from app import controllers
from app import services
from app import models
@app.route('/', methods=['GET', 'POST'])
def listen():
    return jsonify({"message":'Successfully running'})

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    userData = request.get_json()
    try:
         return controllers.AudioController.signup(userData)
    except:
        print("Error")
        

        
@app.route('/login', methods=['GET', 'POST'])
def login():
    userData = request.get_json()
    try:
         return controllers.AudioController.login(userData)
    except:
        print("Error")
        
        
@app.route('/auth', methods=['GET', 'POST'])
def auth():
    try:
         return controllers.AudioController.auth()
    except:
        print("Error")
        




@app.route('/summarize', methods=['GET', 'POST'])
def summary():
    text_obj = request.get_json()
    input_text = text_obj['text']
    stop_words = text_obj['limit']
    top = text_obj['top']
    print(top)
    try:
        processed_text = services.Service.listen(input_text)
        t5_summary = models.SummarizerModel.t5_summarizer(processed_text,stop_words,top)
        lsa = models.SummarizerModel.lsa(input_text,stop_words)
        kl = models.SummarizerModel.kl(input_text,stop_words)
        
        summary = {
            't5_summary':t5_summary,
            'lsa': lsa,
            'kl':kl
        }
        return jsonify({"summary": summary}),200
    except:
        return "Error"