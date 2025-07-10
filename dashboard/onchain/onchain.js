document.addEventListener('DOMContentLoaded', () => {
    const chartsContainer = document.querySelector('.charts-container');

    // Initial update
    updateCharts();

    async function updateCharts() {
        try {
            // Get images from both chains and regions
            const chains = ['eth', 'tron'];
            const regions = ['gl', 'kr'];
            const allImages = [];

            for (const chain of chains) {
                for (const region of regions) {
                    const images = await fetchImages(chain, region);
                    allImages.push(...images);
                }
            }

            displayImages(allImages);
        } catch (error) {
            console.error('Error loading images:', error);
            chartsContainer.innerHTML = '<p>Error loading images</p>';
        }
    }

    function displayImages(images) {
        chartsContainer.innerHTML = '';
    
        // Group images: { tether: { gl: [], kr: [] }, usdc: { gl: [], kr: [] } }
        const grouped = {
            tether: { gl: [], kr: [] },
            usdc: { gl: [], kr: [] }
        };
    
        images.forEach(image => {
            const nameLower = image.name.toLowerCase();
            const folderLower = image.folder.toLowerCase();
    
            const stable = nameLower.includes('tether') ? 'tether'
                          : nameLower.includes('usdc') ? 'usdc'
                          : null;
    
            const region = folderLower.includes('/gl') ? 'gl'
                        : folderLower.includes('/kr') ? 'kr'
                        : null;
    
            if (stable && region && grouped[stable]) {
                grouped[stable][region].push(image);
            }
        });
    
        // Section creation
        function createSection(title, imageGroup) {
            const section = document.createElement('div');
            section.className = 'image-section';
    
            const sectionTitle = document.createElement('h2');
            sectionTitle.textContent = title;
            section.appendChild(sectionTitle);
    
            const row = document.createElement('div');
            row.className = 'chart-row';
    
            const leftCol = document.createElement('div');
            leftCol.className = 'chart-column';
            const rightCol = document.createElement('div');
            rightCol.className = 'chart-column';

            // After creating leftCol
            const leftTitle = document.createElement('h3');
            leftTitle.textContent = 'Global';
            leftCol.appendChild(leftTitle);

            // After creating rightCol
            const rightTitle = document.createElement('h3');
            rightTitle.textContent = 'Korea';
            rightCol.appendChild(rightTitle);
    
            imageGroup.gl.forEach(img => leftCol.appendChild(createChartDiv(img)));
            imageGroup.kr.forEach(img => rightCol.appendChild(createChartDiv(img)));
    
            row.appendChild(leftCol);
            row.appendChild(rightCol);
            section.appendChild(row);
    
            chartsContainer.appendChild(section);
        }
    
        // Image div creation
        function createChartDiv(image) {
            const chartDiv = document.createElement('div');
            chartDiv.className = 'chart';
    
            const img = document.createElement('img');
            img.src = image.path;
            img.alt = image.name;
            img.className = 'chart-image';
            img.onclick = () => openModal(image);
    
            const caption = document.createElement('div');
            caption.className = 'chart-caption';
            caption.innerHTML = `
                <span class="image-name">${image.name}</span><br>
                <span class="image-folder">${image.folder}</span>
            `;
    
            chartDiv.appendChild(img);
            chartDiv.appendChild(caption);
            return chartDiv;
        }
    
        // Display Tether section first, then USDC
        createSection('Tether', grouped.tether);
        createSection('USDC', grouped.usdc);
    }
    

    // Modal functionality
    function openModal(image) {
        const modal = document.getElementById('imageModal');
        const modalImg = document.getElementById('modalImage');
        const captionText = document.getElementById('modalCaption');

        modal.style.display = 'block';
        modalImg.src = image.path;
        captionText.innerHTML = `
            <span class="image-name">${image.name}</span>
            <br>
            <span class="image-folder">${image.folder}</span>
        `;

        // Close modal when clicking the X button
        document.querySelector('.close').onclick = () => {
            modal.style.display = 'none';
        }

        // Close modal when clicking outside
        window.onclick = (event) => {
            if (event.target === modal) {
                modal.style.display = 'none';
            }
        }
    }

    async function fetchImages(chain, region) {
        const images = [];
        const dirPath = `/onchain/${chain}/${region}`;

        try {
            // Get image list from server
            const response = await fetch(`/onchain/${chain}/${region}`);
            if (!response.ok) {
                throw new Error('Failed to fetch images');
            }
            const imageFiles = await response.json();

            // Create image objects with path and name
            imageFiles.forEach(file => {
                const fullPath = `${dirPath}/${file}`;
                const folderPath = fullPath.substring(0, fullPath.lastIndexOf('/'));
                images.push({
                    name: file,
                    path: fullPath,
                    folder: folderPath
                });
            });

            return images;
        } catch (error) {
            console.error('Error fetching images:', error);
            throw error;
        }
    }
});
