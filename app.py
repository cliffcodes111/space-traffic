
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
            body {{background-color: #23272a; color: #fff; font-family: 'Montserrat', Arial, sans-serif; margin: 0; padding: 0; min-height: 100vh;}}
            .container {{display: flex; flex-direction: column; align-items: center; justify-content: center; min-height: 100vh;}}
            .header-row {{display: flex; flex-direction: row; align-items: center; justify-content: center; margin-bottom: 30px;}}
            .orbit-title {{font-family: 'Montserrat', Arial, sans-serif; font-size: 48px; font-weight: 700; color: #82c7a5ff; margin-right: 24px;}}
            .orbit-logo {{height: 64px; width: auto;}}
            h2 {{font-family: 'Montserrat', Arial, sans-serif; font-size: 20px; margin-bottom: 20px; font-weight: 700; letter-spacing: 1px;}}
            .frame-controls {{margin: 20px;}}
            .frame-controls button {{font-size: 16px; padding: 8px 16px; margin: 0 10px; background: #7289da; color: #fff; border: none; border-radius: 4px; cursor: pointer;}}
            .frame-controls span {{font-size: 16px; margin: 0 10px;}}
            .chatbot-container {{margin-top: 40px; width: 100%; max-width: 500px; background: #2c2f33; border-radius: 8px; padding: 20px; box-shadow: 0 2px 8px rgba(0,0,0,0.2);}}
            .chatbot-title {{font-size: 18px; font-weight: 700; margin-bottom: 10px; color: #7289da;}}
            .chatbot-form {{display: flex;}}
            .chatbot-form input {{flex: 1; padding: 8px; border-radius: 4px; border: none; margin-right: 10px;}}
            .chatbot-form button {{padding: 8px 16px; background: #7289da; color: #fff; border: none; border-radius: 4px; cursor: pointer;}}
            .chatbot-response {{margin-top: 15px; color: #fff; font-size: 15px;}}
        </style>
        <script type="text/javascript">
            let running = false;
            let currentFrame = {frame};
            const totalFrames = {total_frames};
            function runAnimation() {{
                if (running) {{ return; }}
                running = true;
                document.getElementById('runBtn').disabled = true;
                animateFrame(currentFrame);
            }}
            function animateFrame(frameNum) {{
                if (!running || frameNum > totalFrames) {{
                    running = false;
                    document.getElementById('runBtn').disabled = false;
                    document.getElementById('refreshBtn').disabled = false;
                    return;
                }}
                fetch('/?frame=' + frameNum)
                    .then(response => response.text())
                    .then(html => {{
                        const parser = new DOMParser();
                        const doc = parser.parseFromString(html, 'text/html');
                        document.getElementById('plot-img').innerHTML = doc.getElementById('plot-img').innerHTML;
                        document.getElementById('frame-label').innerHTML = doc.getElementById('frame-label').innerHTML;
                        setTimeout(function() {{ animateFrame(frameNum + 1); }}, 500);
                    }});
            }}
            function refreshAnimation() {{
                running = false;
                document.getElementById('runBtn').disabled = false;
                document.getElementById('refreshBtn').disabled = true;
                fetch('/?frame=1')
                    .then(response => response.text())
                    .then(html => {{
                        const parser = new DOMParser();
                        const doc = parser.parseFromString(html, 'text/html');
                        document.getElementById('plot-img').innerHTML = doc.getElementById('plot-img').innerHTML;
                        document.getElementById('frame-label').innerHTML = doc.getElementById('frame-label').innerHTML;
                    }});
            }}
            function handleChatbotSubmit(event) {{
                event.preventDefault();
                document.getElementById('chatbot-response').innerText = "Thank you for your question. My chatbot capabilities are still in development, please check again later for orbit-watch insights";
            }}
        </script>
    </head>
    <body>
        <div class="container">
            <div class="header-row">
                <span class="orbit-title">Orbit-Watch interface</span>
            </div>
            <div style="font-family: 'Montserrat', Arial, sans-serif; font-size: 28px; font-weight: 700; color: #82c7a5ff; margin-bottom: 20px;">Space Traffic Control time = {frame}</div>
            <div class="frame-controls">
                <span id="frame-label">Frame {frame} of {total_frames}</span>
                <button id="runBtn" type="button" onclick="runAnimation();">Run</button>
                <button id="refreshBtn" type="button" onclick="refreshAnimation();" disabled>Refresh</button>
            </div>
            <div style="display: flex; flex-direction: row; align-items: flex-start; justify-content: center; width: 100%;">
                <div id="plot-img">{animation_html}</div>
                <div style="margin-left: 40px; background: #23272a; border-radius: 8px; padding: 20px; min-width: 180px; color: #fff; font-family: 'Montserrat', Arial, sans-serif; box-shadow: 0 2px 8px rgba(0,0,0,0.2);">
                    <div style="font-size: 18px; font-weight: 700; margin-bottom: 16px; color: #82c7a5ff;">Legend</div>
                    <div style="display: flex; align-items: center; margin-bottom: 12px;">
                        <svg width="24" height="24" style="margin-right: 8px;"><polygon points="12,4 20,20 4,20" fill="red" /></svg>
                        <span>space junk</span>
                    </div>
                    <div style="display: flex; align-items: center; margin-bottom: 12px;">
                        <svg width="24" height="24" style="margin-right: 8px;"><polygon points="12,2 15,17 2,7 22,7 9,17" fill="green" /><circle cx="12" cy="12" r="2" fill="green" /></svg>
                        <span>commercial transport</span>
                    </div>
                    <div style="display: flex; align-items: center;">
                        <svg width="24" height="24" style="margin-right: 8px;"><circle cx="12" cy="12" r="8" fill="blue" /></svg>
                        <span>space agency satellite</span>
                    </div>
                </div>
            </div>
            <div class="chatbot-container">
                <div class="chatbot-title">Orbit-Watch Chatbot</div>
                <form class="chatbot-form" onsubmit="handleChatbotSubmit(event)">
                    <input type="text" placeholder="Ask a question..." />
                    <button type="submit">Send</button>
                </form>
                <div id="chatbot-response" class="chatbot-response"></div>
            </div>
        </div>
    </body>
    </html>
    """
    return render_template_string(html)
