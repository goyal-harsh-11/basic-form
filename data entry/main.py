import os
import csv
from flask import Flask, send_file, request, render_template, redirect, url_for

def get_form_data():
    form_data = [
        request.form['name'],
        request.form['email'],
        request.form['phone'],
        request.form['education'],
        request.form['occupation']
    ]
    return form_data

def save_form_data(form_data, filename='csv/data.csv'):
    with open(filename, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(form_data)

def get_all_data(filename='csv/data.csv'):
    data = []
    with open(filename, mode='r') as file:
        reader = csv.reader(file)
        for row in reader:
            data.append(row)
    return data

def save_modified_data(data, filename='csv/data.csv'):
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(data)

app = Flask(__name__, template_folder='src')

@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        form_data = get_form_data()
        save_form_data(form_data)
        return redirect(url_for('output'))  # Redirect after saving
    else:
        return send_file('src/index.html')  # Serve index.html for GET requests
@app.route('/output')
def output():
    data = get_all_data()
    return render_template('output.html', data=data)
@app.route('/delete/<int:index>')
def delete_entry(index):
    data = get_all_data()
    if 0 < index <= len(data):
        del data[index - 1]  # Delete the entry (adjust index for 0-based list)
        save_modified_data(data)  # Save the modified data back to CSV
    return redirect(url_for('output'))

def main():
    app.run(debug=True,port=int(os.environ.get('PORT', 80)))

if __name__ == "__main__":
    main()