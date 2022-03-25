# https://docs.python.org/2/library/difflib.html (difflib python Library)
from flask import Flask, render_template, request, flash, redirect, url_for  #Flask
from difflib import SequenceMatcher #SequenceMatcher function of difflib library to check plagiarism
import docx2txt #library to convert microsoft word docx to txt

ALLOWED_EXTENSIONS = {'doc', 'docx'} #allowing extension to upload
#app = Flask(__name__)
app=Flask(__name__,template_folder='templates')
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
@app.after_request
def add_header(response):
    # response.cache_control.no_store = True
    if 'Cache-Control' not in response.headers:
        response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0'
    return response

# function for home page (contain form in it)
@app.route('/')
def index():
    return render_template('index.html')

#function to check plegerism
@app.route('/check', methods=['GET', 'POST'])
def check():
    files = request.files.getlist("file") #getting list of files from html form
    pattern = request.files['pattern'] #getting pattern file from html form
    pos = [] #list of positions of matched text
    found_text = []
    filenames = []
    for f in files: #for loop to compare files one by one with pattern file
        if allowed_file(pattern.filename): #checking if file extension match with uploaded allowed extensions
            pattern_text = docx2txt.process(pattern) #converting pattern file to txt
            text = docx2txt.process(f).splitlines(1) #converting text files to txt
            filenames.append(f"In '{f.filename}' similar pattern not found")
            found = ''
            for lines in text: #for loop to compare different paragraphs
                s = SequenceMatcher(None, lines, pattern_text).ratio()
                percentage = s * 100 #checking percentage of matched text per line
                if percentage > 15:
                    if found != f.filename:
                        found_text.append(f'{f.filename} : {lines}') #getting matched text to show in pattern section
                        round_percentage = round(percentage) #getting matched text percentage
                        pos.append(f"In '{f.filename}' similar pattern found with {round_percentage}% probability")
                        found = f.filename
        else:
            flash("Please upload a valid extension file")
            return redirect(url_for('index'))

    if not found_text:
        pos = filenames
        found_text = ['Similar Pattern not found']

    return render_template('compare.html', pattern_text=found_text, pos=pos)

def allowed_file(filename): # function to check allowed extensions
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

if __name__ == '__main__':
    app.secret_key = 'thisismysecretkey'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.debug = True
    app.run()
    

