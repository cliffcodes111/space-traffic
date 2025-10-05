
import os
from flask import Flask, render_template_string

from connect_plot_to_app import run_app
from flask import request

app = Flask(__name__)

@app.route('/')
def show_plot():
    frame = int(request.args.get('frame', 1))
    animation_html, total_frames = run_app(frame=frame)
    prev_frame = max(1, frame - 1)
    next_frame = min(total_frames, frame + 1)
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
            .frame-controls {{
                margin: 20px;
            }}
            .frame-controls button {{
                font-size: 16px;
                padding: 8px 16px;
                margin: 0 10px;
                background: #7289da;
                color: #fff;
                border: none;
                border-radius: 4px;
                cursor: pointer;
            }}
            .frame-controls span {{
                font-size: 16px;
                margin: 0 10px;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h2>Today's LEO traffic</h2>
            <div class="frame-controls">
                <form method="get" style="display:inline;">
                    <input type="hidden" name="frame" value="{prev_frame}">
                    <button type="submit">Previous</button>
                </form>
                <span>Frame {frame} of {total_frames}</span>
                <form method="get" style="display:inline;">
                    <input type="hidden" name="frame" value="{next_frame}">
                    <button type="submit">Next</button>
                </form>
            </div>
            {animation_html}
        </div>
    </body>
    </html>
    """
    return render_template_string(html)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
    