
import os
from flask import Flask, render_template_string
from connect_plot_to_app import run_app

app = Flask(__name__)

@app.route('/')
def show_plot():
    animation_html = run_app()
    html = f"""
    <html>
    <head>
        <link href='https://fonts.googleapis.com/css?family=Montserrat:400,700' rel='stylesheet'>
        <style>
            body {{
                background-color: #23272a;
                color: #fff;
                font-family: 'Montserrat', Arial, sans-serif;
                margin: 0;
                padding: 0;
                min-height: 100vh;
            }}
            .container {{
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                min-height: 100vh;
            }}
            h2 {{
                font-family: 'Montserrat', Arial, sans-serif;
                font-size: 20px;
                margin-bottom: 20px;
                font-weight: 700;
                letter-spacing: 1px;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h2>Space Traffic Plot</h2>
            {animation_html}
        </div>
    </body>
    </html>
    """
    return render_template_string(html)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
    