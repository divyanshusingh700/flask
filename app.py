from flask import Flask,flash,send_from_directory,render_template,request,redirect,url_for
import os,configuration
from werkzeug.utils import secure_filename
from query import Process_csv

app = Flask(__name__)
app.secret_key = configuration.SECRET_KEY


# Upload folder
UPLOAD_FOLDER = 'user_upload/'
app.config['UPLOAD_FOLDER'] =  UPLOAD_FOLDER

# This method will limit the users to upload only csv file
ALLOWED_EXTENSIONS = {'csv'}
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Get the uploaded files
@app.route("/", methods=['GET','POST'])
def uploadFiles():

    if request.method == 'POST':  

        # Check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        
        file = request.files['file']

        # If the user does not select a file, the browser submits an
        # Empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path) # Saving the uploaded file from client to user_upload directory
            obj=Process_csv(file_path) #Creating an instance of Process_csv class
            obj.json_to_csv() # Call json to csv method 
            return redirect(url_for('get_matched_products'))
    return render_template('index.html')

# Rendering page of download csv after getting redirecting from home page
@app.route('/get_matched_products')
def get_matched_products():
    return render_template('download.html', files=os.listdir('output/'))

# Sending converted csv files from download directory to users in a url format
@app.route('/get_matched_products/<filename>')
def download_file(filename):
    return send_from_directory('output/', filename)

if __name__=="__main__":

    # Enable debugging mode
    app.config["DEBUG"] = True
    app.run(port=5000)
