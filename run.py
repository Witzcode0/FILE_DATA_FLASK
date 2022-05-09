from flask import Flask, flash, jsonify, redirect, render_template, request
import os
import urllib.request
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['SECRET_KEY'] = "9387rgfbndro84u4edtcy"
app.config['UPLOAD_FOLDER'] = "D:\\3-Flask\\Complete project\\File-data\\uploads"
app.config['MAX_CONTENT_LENGTH'] = 16*1024*1024

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
    ex = filename.rsplit('.',1)[1].lower()
    dot = '.' in filename 
    result = dot and ex in ALLOWED_EXTENSIONS 
    return result

@app.route("/")
def upload_form():
	files = os.listdir(app.config['UPLOAD_FOLDER'])
	return render_template("upload.html", files=files)

@app.route("/singlefile", methods=["POST"])
def upload_file():
	if request.method == "POST":
		if 'file' not in request.files:
			flash("no file [multipart/form-data]")
			return redirect(request.url)
		file = request.files['file']

		if file.filename == '':
			flash('No file selected for uploading')
			return redirect(request.url)

		if file and allowed_file(file.filename):
			filename = secure_filename(file.filename)
			file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
			flash("File successfully uploaded")
			return redirect("/")
		else:
			flash('Allowed file types are txt,pdf,png,jpg,jpeg,gif')
			return redirect(request.url)

@app.route('/multiplefiles', methods=["POST"])
def multi_upload_file():
	if request.method == "POST":
		if 'files[]' not in request.files:
			flash("no file [multipart/form-data]")
			return redirect(request.url)
		files = request.files.getlist('files[]')
		print(files)
		for file in files:
			print(file, '1')
			if file and allowed_file(file.filename):
				print(file)
				filename = secure_filename(file.filename)
				file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
		flash("File(s) successfully uploaded")
		return redirect("/")

@app.route("/restapiuploadmultifile", methods=["POST"])
def rest_api_upload_multi_file():
	if 'files[]' not in request.files:
		resp = jsonify({'message': 'No file part in the request'})
		resp.status_code = 400
		return resp
	files = request.files.getlist('files[]')
	errors = {}
	success = False
	for file in files:
		if file and allowed_file(file.filename):
			filename = secure_filename(file.filename)
			file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
			success = True
		else:
			errors[file.filename] = "File type is not allowed"
	if success and errors:
		errors['message'] = "file(s) successfully uploaded"
		resp = jsonify(errors)
		resp.status_code = 500
		return resp
	if success:
		resp = jsonify({'message':'files successfully uploaded'})
		resp.status_code = 201
		return resp
	else:
		resp = jsonify(errors)
		resp.status_code = 500
		return resp


if __name__ == "__main__":
	app.run(debug=True, port=8000)