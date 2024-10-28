const video = document.getElementById('video');
const captureButton = document.getElementById('capture');
const jsonResult = document.getElementById('jsonResult');

// Access webcam
navigator.mediaDevices.getUserMedia({ video: true })
    .then(stream => {
        video.srcObject = stream;
    })
    .catch(error => {
        console.error("Error accessing webcam:", error);
    });

captureButton.addEventListener('click', () => {
    const canvas = document.createElement('canvas');
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    const context = canvas.getContext('2d');
    context.drawImage(video, 0, 0, canvas.width, canvas.height);

    // Convert image to base64
    const imageData = canvas.toDataURL('image/jpeg');

    // Send image to Flask app
    fetch('/analyze', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ image: imageData })
    })
    .then(response => response.json())
    .then(data => {
        jsonResult.textContent = JSON.stringify(data, null, 2);
    })
    .catch(error => console.error("Error:", error));
});
