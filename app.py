from flask import Flask, render_template_string
import matplotlib.pyplot as plt
from io import BytesIO
import base64

app = Flask(__name__)

@app.route('/')
def show_plot():
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot([1, 2, 3], [4, 5, 6])  # Example plot

    buf = BytesIO()
    fig.savefig(buf, format="png")
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    html = f"<h2>Space Traffic Plot</h2><img src='data:image/png;base64,{data}'/>"
    print( "access the app on http://<20.162.192.119>:5000")
    return render_template_string(html)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
    