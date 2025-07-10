// Configuration
const figuresDir = 'figure/';
const figureGrid = document.getElementById('figureGrid');

function extractDateRange(filename) {
    const match = filename.match(/price_error_(\d{4}-\d{2}-\d{2})_(\d{4}-\d{2}-\d{2})\.png/);
    return match ? { startDate: match[1], endDate: match[2] } : null;
}

function createModal(content) {
    const modal = document.createElement('div');
    modal.className = 'modal-overlay';

    const fullCard = content.cloneNode(true);
    fullCard.className = 'image-card full-screen';

    const closeButton = document.createElement('button');
    closeButton.className = 'close-button';
    closeButton.textContent = '×';
    closeButton.onclick = () => document.body.removeChild(modal);
    fullCard.appendChild(closeButton);

    modal.appendChild(fullCard);
    document.body.appendChild(modal);

    modal.onclick = (e) => {
        if (e.target === modal) {
            document.body.removeChild(modal);
        }
    };

    const escHandler = (e) => {
        if (e.key === 'Escape') {
            document.body.removeChild(modal);
            document.removeEventListener('keydown', escHandler);
        }
    };
    document.addEventListener('keydown', escHandler);
}

function createImageCard(pair, exchange, imagePath, filename) {
    const dates = extractDateRange(filename);
    if (!dates) {
        console.error(`Invalid filename format: ${filename}`);
        return null;
    }

    const card = document.createElement('div');
    card.className = 'image-card';

    const img = document.createElement('img');
    img.src = imagePath;
    img.alt = `${pair} ${exchange} price error (${dates.startDate} to ${dates.endDate})`;
    img.onerror = () => {
        console.error(`Failed to load image: ${imagePath}`);
        img.src = 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg==';
    };

    const caption = document.createElement('div');
    caption.className = 'caption';
    caption.innerHTML = `
        <p>${pair} - ${exchange}</p>
        <p class="date-range">${dates.startDate} to ${dates.endDate}</p>
    `;

    card.appendChild(img);
    card.appendChild(caption);

    card.addEventListener('click', () => createModal(card.firstChild));
    return card;
}

async function loadImages() {
    figureGrid.innerHTML = '';

    try {
        const pairs = await fetch('/api/pairs').then(res => res.json());
        const exchanges = await fetch('/api/exchanges').then(res => res.json());

        for (const pair of pairs) {
            const pairSection = document.createElement('div');
            pairSection.className = 'pair-section';

            const header = document.createElement('h2');
            header.textContent = pair;
            pairSection.appendChild(header);

            const grid = document.createElement('div');
            grid.className = 'grid-container';

            for (const exchange of exchanges) {
                try {
                    const files = await fetch(`/api/files/${pair}/${exchange}`).then(res => res.json());

                    for (const filename of files) {
                        const imagePath = `/figure/${pair}/upbit/${exchange}/${filename}`;
                        const card = createImageCard(pair, exchange, imagePath, filename);
                        if (card) grid.appendChild(card);
                    }
                } catch (err) {
                    console.error(`Error fetching files for ${pair}/upbit/${exchange}:`, err);
                }
            }

            pairSection.appendChild(grid);
            figureGrid.appendChild(pairSection);
        }
    } catch (error) {
        console.error('Error loading images:', error);
    }
}

    
window.addEventListener('load', loadImages);
