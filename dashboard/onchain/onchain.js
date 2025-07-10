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
        
        images.forEach((image, index) => {
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
                <span class="image-name">${image.name}</span>
                <br>
                <span class="image-folder">${image.folder}</span>
            `;
            
            chartDiv.appendChild(img);
            chartDiv.appendChild(caption);
            chartsContainer.appendChild(chartDiv);
        });
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
