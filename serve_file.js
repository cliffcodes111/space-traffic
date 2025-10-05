const express = require('express');
const fs = require('fs');
const path = require('path');

const app = express();
const PORT = process.env.PORT || 8081;

app.get('/connect_plot_to_app.py', (req, res) => {
    const filePath = path.join(__dirname, 'connect_plot_to_app.py');
    fs.readFile(filePath, 'utf8', (err, data) => {
        if (err) {
            res.status(404).send('File not found');
        } else {
            res.send(`<!DOCTYPE html><html><body><h2>connect_plot_to_app.py</h2><pre>${data}</pre></body></html>`);
        }
    });
});

app.use((req, res) => {
    res.status(404).send('Not Found');
});

app.listen(PORT, () => {
    console.log(`Serving on http://localhost:${PORT}/connect_plot_to_app.py`);
});
