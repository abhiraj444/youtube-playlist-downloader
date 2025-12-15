// YouTube Playlist Extractor - Frontend Logic

// State management
let playlistData = null;
let generatedContent = null;
let fileId = null;

// DOM Elements
const playlistUrl = document.getElementById('playlistUrl');
const defaultQuality = document.getElementById('defaultQuality');
const fetchBtn = document.getElementById('fetchBtn');
const errorMessage = document.getElementById('errorMessage');

const videoSection = document.getElementById('videoSection');
const playlistTitle = document.getElementById('playlistTitle');
const videoCount = document.getElementById('videoCount');
const videoList = document.getElementById('videoList');
const selectAllBtn = document.getElementById('selectAllBtn');
const deselectAllBtn = document.getElementById('deselectAllBtn');
const selectedCount = document.getElementById('selectedCount');
const generateBtn = document.getElementById('generateBtn');
const progressBar = document.getElementById('progressBar');
const progressFill = document.getElementById('progressFill');
const progressText = document.getElementById('progressText');

const downloadSection = document.getElementById('downloadSection');
const totalVideos = document.getElementById('totalVideos');
const successCount = document.getElementById('successCount');
const failedCount = document.getElementById('failedCount');
const failedStat = document.getElementById('failedStat');
const copyBtn = document.getElementById('copyBtn');
const downloadBtn = document.getElementById('downloadBtn');
const previewContent = document.getElementById('previewContent');
const copySuccess = document.getElementById('copySuccess');
const resetBtn = document.getElementById('resetBtn');

// Utility Functions
function showError(message) {
    errorMessage.textContent = message;
    errorMessage.style.display = 'block';
    setTimeout(() => {
        errorMessage.style.display = 'none';
    }, 5000);
}

function formatDuration(seconds) {
    if (!seconds) return 'N/A';
    const hours = Math.floor(seconds / 3600);
    const minutes = Math.floor((seconds % 3600) / 60);
    const secs = seconds % 60;

    if (hours > 0) {
        return `${hours}:${String(minutes).padStart(2, '0')}:${String(secs).padStart(2, '0')}`;
    }
    return `${minutes}:${String(secs).padStart(2, '0')}`;
}

function updateSelectedCount() {
    const checkboxes = document.querySelectorAll('.video-checkbox');
    const checked = Array.from(checkboxes).filter(cb => cb.checked).length;
    selectedCount.textContent = `${checked} selected`;
    generateBtn.style.display = checked > 0 ? 'block' : 'none';
}

// Event Handlers
fetchBtn.addEventListener('click', async () => {
    const url = playlistUrl.value.trim();

    if (!url) {
        showError('Please enter a playlist URL');
        return;
    }

    if (!url.includes('list=')) {
        showError('Invalid playlist URL. Make sure it contains "list=" parameter');
        return;
    }

    // Show loading state
    fetchBtn.disabled = true;
    fetchBtn.querySelector('.btn-text').textContent = 'Fetching...';
    fetchBtn.querySelector('.spinner').style.display = 'inline';
    errorMessage.style.display = 'none';

    try {
        const response = await fetch('/api/fetch-playlist', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                url: url,
                default_quality: defaultQuality.value
            })
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Failed to fetch playlist');
        }

        playlistData = await response.json();
        displayPlaylist(playlistData);

    } catch (error) {
        showError(error.message);
    } finally {
        fetchBtn.disabled = false;
        fetchBtn.querySelector('.btn-text').textContent = 'Fetch Playlist';
        fetchBtn.querySelector('.spinner').style.display = 'none';
    }
});

function displayPlaylist(data) {
    playlistTitle.textContent = data.title;
    videoCount.textContent = `${data.total_videos} videos`;

    videoList.innerHTML = '';

    data.videos.forEach((video, index) => {
        const videoItem = document.createElement('div');
        videoItem.className = 'video-item';

        videoItem.innerHTML = `
            <input type="checkbox" class="video-checkbox" data-video-id="${video.id}" checked>
            <img src="${video.thumbnail}" alt="${video.title}" class="video-thumbnail">
            <div class="video-info">
                <div class="video-title">${video.title}</div>
                <div class="video-duration">Duration: ${formatDuration(video.duration)}</div>
            </div>
            <select class="video-quality-select" data-video-id="${video.id}">
                <option value="best" ${defaultQuality.value === 'best' ? 'selected' : ''}>Best</option>
                <option value="1080p" ${defaultQuality.value === '1080p' ? 'selected' : ''}>1080p</option>
                <option value="720p" ${defaultQuality.value === '720p' ? 'selected' : ''}>720p</option>
                <option value="480p" ${defaultQuality.value === '480p' ? 'selected' : ''}>480p</option>
                <option value="360p" ${defaultQuality.value === '360p' ? 'selected' : ''}>360p</option>
            </select>
        `;

        videoList.appendChild(videoItem);
    });

    // Add event listeners to checkboxes
    document.querySelectorAll('.video-checkbox').forEach(cb => {
        cb.addEventListener('change', updateSelectedCount);
    });

    videoSection.style.display = 'block';
    updateSelectedCount();

    // Scroll to video section
    videoSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

selectAllBtn.addEventListener('click', () => {
    document.querySelectorAll('.video-checkbox').forEach(cb => {
        cb.checked = true;
    });
    updateSelectedCount();
});

deselectAllBtn.addEventListener('click', () => {
    document.querySelectorAll('.video-checkbox').forEach(cb => {
        cb.checked = false;
    });
    updateSelectedCount();
});

generateBtn.addEventListener('click', async () => {
    const checkboxes = document.querySelectorAll('.video-checkbox:checked');

    if (checkboxes.length === 0) {
        showError('Please select at least one video');
        return;
    }

    // Collect selected videos with their qualities
    const selectedVideos = Array.from(checkboxes).map(cb => {
        const videoId = cb.dataset.videoId;
        const video = playlistData.videos.find(v => v.id === videoId);
        const qualitySelect = document.querySelector(`.video-quality-select[data-video-id="${videoId}"]`);

        return {
            id: videoId,
            title: video.title,
            quality: qualitySelect.value
        };
    });

    // Show loading state
    generateBtn.disabled = true;
    generateBtn.querySelector('.btn-text').textContent = 'Generating...';
    generateBtn.querySelector('.spinner').style.display = 'inline';
    progressBar.style.display = 'block';
    progressFill.style.width = '0%';
    progressText.textContent = 'Processing videos...';

    // Simulate progress (since we're using concurrent processing)
    let progress = 0;
    const progressInterval = setInterval(() => {
        progress += 5;
        if (progress <= 90) {
            progressFill.style.width = `${progress}%`;
            progressText.textContent = `Processing ${selectedVideos.length} videos...`;
        }
    }, 200);

    try {
        const response = await fetch('/api/generate-urls', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                videos: selectedVideos
            })
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Failed to generate URLs');
        }

        const result = await response.json();

        clearInterval(progressInterval);
        progressFill.style.width = '100%';
        progressText.textContent = 'Complete!';

        setTimeout(() => {
            displayResults(result);
        }, 500);

    } catch (error) {
        clearInterval(progressInterval);
        showError(error.message);
        progressBar.style.display = 'none';
    } finally {
        generateBtn.disabled = false;
        generateBtn.querySelector('.btn-text').textContent = 'Generate Download Links';
        generateBtn.querySelector('.spinner').style.display = 'none';
    }
});

function displayResults(result) {
    generatedContent = result.content;
    fileId = result.file_id;

    totalVideos.textContent = result.total_successful + result.total_failed;
    successCount.textContent = result.total_successful;

    if (result.total_failed > 0) {
        failedCount.textContent = result.total_failed;
        failedStat.style.display = 'block';
    } else {
        failedStat.style.display = 'none';
    }

    // Show preview (first 3 URLs)
    const lines = result.content.split('\n');
    const previewLines = [];
    let urlCount = 0;

    for (const line of lines) {
        previewLines.push(line);
        if (line.startsWith('http')) {
            urlCount++;
            if (urlCount >= 3) break;
        }
    }

    previewContent.textContent = previewLines.join('\n') + '\n\n... and more';

    downloadSection.style.display = 'block';
    progressBar.style.display = 'none';

    // Scroll to download section
    downloadSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

copyBtn.addEventListener('click', async () => {
    try {
        await navigator.clipboard.writeText(generatedContent);
        copySuccess.style.display = 'block';
        copyBtn.textContent = '✅ Copied!';

        setTimeout(() => {
            copySuccess.style.display = 'none';
            copyBtn.textContent = '📋 Copy to Clipboard';
        }, 3000);
    } catch (error) {
        showError('Failed to copy to clipboard. Please try downloading instead.');
    }
});

downloadBtn.addEventListener('click', () => {
    window.location.href = `/download/${fileId}`;
});

resetBtn.addEventListener('click', () => {
    // Reset all state
    playlistData = null;
    generatedContent = null;
    fileId = null;

    playlistUrl.value = '';
    defaultQuality.value = 'best';

    videoSection.style.display = 'none';
    downloadSection.style.display = 'none';

    videoList.innerHTML = '';

    // Scroll to top
    window.scrollTo({ top: 0, behavior: 'smooth' });
});

// Allow Enter key to submit URL
playlistUrl.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        fetchBtn.click();
    }
});
