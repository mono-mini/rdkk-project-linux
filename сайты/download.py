from flask import Flask, render_template_string

app = Flask(__name__)

@app.route('/')
def home():
    return render_template_string('''
    <!DOCTYPE html>
    <html>
        <head>
            <meta charset="UTF-8">
            <title><b>download rdkk</b></title>
        </head>
        <body>
            <h1 title="download rdkk" href="./'1 основа'">download rdkk</h1>

        </body>
    </html>
    ''')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)