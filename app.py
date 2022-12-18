from flask import Flask, render_template, request
from flask import escape
import pickle
import random
app = Flask(__name__)

class NaiveApp:
    def __init__(self):
        self.model = pickle.load(open('models/model.pkl', 'rb'))
        self.transformer = pickle.load(open("models/tfr.pkl", 'rb'))
        self.imgs  = [
            '../static/img/explain.png',
            '../static/img/explain2.png',
            '../static/img/playing.png',
        ]
        self.random_img = None
    def process_input(self, req: 'flask_request') -> 'html':
        '''This function extracts a value from a POST request and returns the value as a list.'''
        snippet = escape(req.form['message'])
        return [snippet]

    def classify_text(self, req: 'flask_request') -> 'html':
        '''This function classifies a snippet extracted from a POST request as spam or ham.'''
        data = self.process_input(req)
        vec = self.transformer.transform(data)
        pred = self.model.predict(vec)
        print('type of pred is:', type(pred), pred)
        print("DATA ", data)
        return pred, data
    def random_emote(self):
        b = random.randint(0, len(self.imgs)-1)
        self.random_img = self.imgs[b]
        return self.random_img
webapp =  NaiveApp()
@app.route('/',methods=['GET'])
def Home():
    random_scene = ['scence1','scence2','scence3']
    B = random.randint(0,len(random_scene)-1)
    robot_doing = {
        'scence1': {
            'header': 'Robot is currently Dancing now',
            'img':    '../static/img/dancing.gif'
        },
        'scence2': {
            'header': 'Robot is currently Fixing something...',
            'img': '../static/img/fixing.png'
        },
        'scence3': {
            'header': 'Robot is currently Thinking something...',
            'img': '../static/img/thinking.png'
        }
    }
    currentScene = robot_doing[random_scene[B]]
    return render_template('index.html',
                           text_class="",
                           detailed_response=currentScene['header'],
                           snippet="",
                           img_path=currentScene['img'],
                           button_text="",
                           no_input=False
                           )


@ app.route('/predict', methods=['POST'])
def predict():
    title = 'Could not classify text'
    text_class = ''
    snippet = ''
    details = ''
    message = ''
    if request.method == "POST":
        message = request
        try:
            pred, data = webapp.classify_text(message)
            if pred == 1:
                text_class = 'Your message is a SPAM'
                title = 'It is spam.'
            else:
                text_class = 'Your message is not a SPAM'
                title = 'It is not spam.'
            snippet = ''.join(data)
        except Exception as e:
            print('Theres something wrong....')
            print(e)
        b = 'a' if pred == 1 else 'no'
        details = f'The text that you gave us for classification has ' + b + '  chance of being spam';
        img_path = webapp.random_emote()
        return render_template('index.html',
                                text_class=text_class,
                                detailed_response=details,
                                snippet=snippet,
                                img_path=img_path,
                                button_text="START OVER",
                                no_input=False
                               )


if __name__ == "__main__":
    #app.run(debug=True, host='0.0.0.0', port='5000')
    app.run(debug=True)