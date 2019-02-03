from flask import Flask, request, render_template, make_response
from flask import Markup, flash
import spacy
from spacy import displacy
import en_core_web_sm

nlp = en_core_web_sm.load()
nlp = spacy.load('en_core_web_sm')


app = Flask(__name__)

@app.route('/')
def my_form():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def my_form_post():
    text = request.form['text']
    print(text)
    doc = nlp(text)
    print([(X.text, X.label_) for X in doc.ents])
    svg = displacy.render(doc, style='ent')
    svg = Markup(svg)
    flash(svg)

    return render_template('index.html')

@app.route('/entity', methods=['GET', 'POST'])
def my_form_get():
    t = request.args.get('input',default=None, type=str)
    print(type(t))
 
    text = str(t.encode('utf-8'))
    doc = nlp(text)

    print([(X.text, X.label_) for X in doc.ents])
    svg = displacy.render(doc, style='ent', minify=True)

    svg = svg.replace(">b'",">").replace("'</","</")
    resp =  make_response(svg)
    resp.mimetype = 'text/plain'
    return resp

if __name__ == '__main__':
	import os
	app.config['SECRET_KEY'] = os.urandom(24).hex()
	app.run(host='0.0.0.0',debug=True)
