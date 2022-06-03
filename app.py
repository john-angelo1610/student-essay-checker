# https://docs.python.org/2/library/difflib.html (difflib python Library)
from flask import Flask, render_template, request, flash, redirect, url_for  # Flask
from difflib import SequenceMatcher  # SequenceMatcher function of difflib library to check plegerism
import docx2txt  # library to convert microsoft word docx to txt

ALLOWED_EXTENSIONS = {'doc', 'docx'}  # allowing extension to upload
app = Flask(__name__)
app.secret_key = 'thisismysecretkey'
app.config['SECRET_KEY'] = 'thisismysecretkeyparttwo'
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_PERMANENT']= False

# function for home page (contain form in it)
@app.route('/')
def index():
    return render_template('index.html')


# function to check plegerism
@app.route('/check', methods=['GET', 'POST'])
def check():
    files = request.files.getlist("file")  # getting list of files from html form
    pattern = request.files['pattern']  # getting pattern file from html form
    pos = []  # list of positions of matched text
    found_text = []
    filenames = []
    for f in files:  # for loop to compare files one by one with pattern file
        if allowed_file(pattern.filename) and allowed_file(
                f.filename):  # checking if file extension match with uploaded allowed extensions
            pattern_text = docx2txt.process(pattern)  # converting pattern file to txt
            text = docx2txt.process(f).splitlines(1)  # converting text files to txt
            filenames.append(f"In '{f.filename}' similar pattern not found")
            # found = ''
            print(pattern_text, 'pattern')
            for lines in text:  # for loop to compare different paragraphs
                s = SequenceMatcher(None, lines, pattern_text).ratio()
                percentage = s * 100  # checking percentage of matched text per line
                if percentage > 10: # change this percentage to match percentage
                # if found == f.filename and percentage > 15:
                    found_text.append(f'{f.filename} : {lines}')  # getting matched text to show in pattern section
                    round_percentage = round(percentage)  # getting matched text percentage
                    pos.append(f"In '{f.filename}' similar pattern found with {round_percentage}% probability")
                    # found = f.filename
        else:
            flash("Please upload a valid extension file")
            return redirect(url_for('index'))

    if not found_text:
        pos = filenames
        found_text = ['Similar Pattern not found']

    return render_template('compare.html', pattern_text=found_text, pos=pos, pattern_name=pattern.filename)


def allowed_file(filename):  # function to check allowed extensions
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



if __name__ == '__main__':
    app.secret_key = 'thisismysecretkey'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.debug = True
    app.run()
