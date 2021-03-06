import os
from flask import Flask, request, session, g, redirect, url_for, abort, \
    render_template, flash, jsonify
from flask_cors import CORS, cross_origin
from werkzeug.utils import secure_filename
from .file_tools import ContentManager

app = Flask(__name__) # create the application instance :)
app.config.from_object(__name__) # load config from this file , flaskr.py
# Load default config and override config from an environment variable
app.config.update(dict(
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='default',
    CORS_HEADER='Content-Type'
))
app.config.from_envvar('NODE_SETTINGS', silent=True)

# Initialize the content manager
cm = ContentManager()
cors = CORS(app, resources={r"/*": {"origins": "*"}})

#max filesize for uploads
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

@app.route('/')
def show_index():
    return 'pyXain API running!'

@app.route('/init/arxain', methods=["GET"])
def init_arxain():
    results = cm.init_arxain();
    return jsonify(results)

@app.route('/init/author', methods=["GET"])
def init_author():
    author_id = request.args.get('author_id')
    print('/init/author triggered with author_id:')
    print(author_id)

    results = cm.init_author(author_id)
    return jsonify(results)

@app.route('/submit/manuscript', methods=["GET"])
def submit_manuscript():
    author_id = request.args.get('author_id')
    paper_id = request.args.get('paper_id')
    paper_directory = request.args.get('paper_directory')

    results = cm.submit_manuscript(author_id, paper_id, paper_directory)

    return jsonify(results)

@app.route('/submit/revision', methods=["GET"])
def submit_revision():
    author_id = request.args.get('author_id')
    paper_id = request.args.get('paper_id')
    paper_directory = request.args.get('paper_directory')

    results = cm.submit_revision(author_id, paper_id, paper_directory)

    return jsonify(results)

@app.route('/submit/comment', methods=["GET"])
def submit_comment():
    author_id = request.args.get('author_id')
    paper_id = request.args.get('paper_id')
    comment_directory = request.args.get('comment_directory')

    results = cm.submit_comment(author_id, paper_id, comment_directory)

    return jsonify(results)

@app.route('/pin/manuscript', methods=["GET"])
def pin_manuscript():
    return 'reserved for future use'

@app.route('/upload/file', methods=['GET','POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'paper' not in request.files:
            flash('No file part named paper.')
            file_present = False

        file = request.files['paper']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            file_present = False
        if file and allowed_file(file.filename):
            #make an upload dir if it doesn't exist
            folder = cm.arxain_path+'/upload'
            if not os.path.exists(folder):
                    os.makedirs(folder)
            #delete files already in upload folder
            for the_file in os.listdir(folder):
                file_path = os.path.join(folder, the_file)
                try:
                    if os.path.isfile(file_path):
                        os.unlink(file_path)
                except Exception as e:
                    print(e)
            #copy file to upload folder
            filename = secure_filename(file.filename)
            file.save(os.path.join(cm.arxain_path, 'upload', filename))
            file_path = cm.arxain_path+'/upload'
            print(file_path)
            file_present = True

        # handle the case if a non allowed file was submitted
        else :
            file_present = False
            file_path = 'failed'
            filename = 'failed'

    results = {}
    results['Success'] = file_present
    results['fileDirectory'] = file_path
    results['fileName'] = filename

    return jsonify(results)
def allowed_file(filename):
    ALLOWED_EXTENSIONS = set(['txt','pdf','json'])
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

if __name__ == "__main__":
    app.debug = True
    app.run(port=5000)
