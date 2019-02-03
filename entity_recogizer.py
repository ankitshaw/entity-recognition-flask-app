from flask import Flask, request, render_template
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
    doc = nlp(text)
    print([(X.text, X.label_) for X in doc.ents])
    svg = displacy.render(doc, style='ent')
    svg = Markup(svg)
    flash(svg)

    return render_template('index.html')

if __name__ == '__main__':
	import os
	app.config['SECRET_KEY'] = os.urandom(24).hex()
	app.run()
