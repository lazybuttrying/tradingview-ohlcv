const express = require('express');
const path = require('path');
const fs = require('fs');

const app = express();
const port = 3000;

const DASHBOARD_DIR = path.join(__dirname, 'dashboard');
const FIGURE_DIR = path.join(DASHBOARD_DIR, 'figure');

app.use(express.static(DASHBOARD_DIR));
app.use('/figure', express.static(FIGURE_DIR));

app.get('/', (req, res) => {
    res.sendFile(path.join(DASHBOARD_DIR, 'figures.html'));
});

app.get('/api/pairs', (req, res) => {
    try {
        const pairs = fs.readdirSync(FIGURE_DIR);
        res.json(pairs);
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

app.get('/api/exchanges', (req, res) => {
    try {
        const pairs = fs.readdirSync(FIGURE_DIR);
        if (pairs.length === 0) return res.json([]);

        const exchangeDir = path.join(FIGURE_DIR, pairs[0], 'upbit');
        const items = fs.readdirSync(exchangeDir);
        const exchanges = items.filter(item =>
            fs.statSync(path.join(exchangeDir, item)).isDirectory()
        );

        res.json(exchanges);
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

app.get('/api/files/:pair/:exchange', (req, res) => {
    try {
        const { pair, exchange } = req.params;
        const dirPath = path.join(FIGURE_DIR, pair, 'upbit', exchange);
        const files = fs.readdirSync(dirPath).filter(file => file.endsWith('.png'));
        res.json(files);
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

app.listen(port, '0.0.0.0', () => {
    console.log(`Server running at http://localhost:${port}`);
});