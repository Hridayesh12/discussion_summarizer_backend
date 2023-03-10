from flask import jsonify, request
from app import app
from app import controllers
from app import services
from app import models
from flask_jwt_extended import create_access_token, get_jwt, get_jwt_identity,unset_jwt_cookies, jwt_required, JWTManager

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
        
@app.route('/gsignup', methods=['GET', 'POST'])
def gsignup():
    userData = request.get_json()
    try:
         return controllers.AudioController.gsignup(userData)
    except:
        print("Error")
        

        
@app.route('/login', methods=['GET', 'POST'])
def login():
    print(request.get_json())
    userData = request.get_json()
    print("User Data",userData)
    try:
         return controllers.AudioController.login(userData)
    except:
        print("Error")
        
@app.route('/glogin', methods=['GET', 'POST'])
def glogin():
    userData = request.get_json()
    try:
         return controllers.AudioController.glogin(userData)
    except:
        print("Error")
        
@app.route('/logout', methods=['GET', 'POST'])
@jwt_required()
def logout():
    try:
         return controllers.AudioController.logout()
    except:
        print("Error")
        
        
@app.route('/title', methods=['GET', 'POST'])
def title():
    sum = request.get_json()
    text=sum['text']
    try:
         return models.SummarizerModel.title(text)
    except:
        print("Error")
        
        
@app.route('/auth', methods=['GET', 'POST'])
def auth():
    try:
         return controllers.AudioController.auth()
    except:
        print("Error")
        
        
@app.route('/save_summary', methods=['GET', 'POST'])
def save_summary():
    mail = request.get_json()
    u_mail=mail['email']
    summ=mail['sum']
    try:
        return controllers.AudioController.save_summary(u_mail,summ)
    except:
        print("Error")
        
@app.route('/video', methods=['GET', 'POST'])
def video():
    print(request)
    vid = request.files['file']
    try:
        print("hi")
        return models.SummarizerModel.video(vid)
    except:
        print("Error")
        
@app.route('/eprofile', methods=['GET', 'POST'])
def eprofile():
    user_data=request.get_json()
    try:
        return controllers.AudioController.eprofile(user_data)
    except:
        print("Error")
        
@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    umail=request.get_json()
    email=umail['email']
    try:
        return controllers.AudioController.forgot_password(email)
    except:
        print("Error")

@app.route('/reset_password', methods=['GET', 'POST'])
@jwt_required()
def reset_password():
    pass_word=request.get_json()
    password=pass_word['password']
    cpassword=pass_word['cpassword']
    token = pass_word['token']
    try:
        return controllers.AudioController.reset_password(password,cpassword,token)
    except:
        print("Error")


@app.route('/summarize', methods=['GET', 'POST'])
def summary():
    text_obj = request.get_json()
    input_text = text_obj['text']
    num_sent = text_obj['num_sent']
    try:
        processed_text = services.Service.listen(input_text)
        # gpt = models.SummarizerModel.gpt(input_text)
        lsa= models.SummarizerModel.lsa(input_text,num_sent)
        kl = models.SummarizerModel.kl(input_text,num_sent)
        title=models.SummarizerModel.title(input_text)
        summary = {
            'lsa': lsa,
            'kl':kl,
            'title': title,
        }
        return jsonify({"summary": summary}),200
    except Exception as e:
            print('kl',e)
            return 'error'