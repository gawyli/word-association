let mediaRecorder;
let audioChunks = [];
let audioBlob;
let audioUrl;

const recordButton = document.getElementById('record-button');
const playButton = document.getElementById('play-button');
const playStimulusButton = document.getElementById('play-stimulus');

recordButton.addEventListener('click', toggleRecording);
playButton.addEventListener('click', playRecording);
playStimulusButton.addEventListener('click', playStimulus);

function toggleRecording() {
    if (mediaRecorder && mediaRecorder.state === 'recording') {
        mediaRecorder.stop();
        recordButton.textContent = 'Record Response';
    } else {
        navigator.mediaDevices.getUserMedia({ audio: true })
            .then(stream => {
                mediaRecorder = new MediaRecorder(stream);
                mediaRecorder.start();
                recordButton.textContent = 'Stop Recording';

                mediaRecorder.addEventListener('dataavailable', event => {
                    audioChunks.push(event.data);
                });

                mediaRecorder.addEventListener('stop', () => {
                    audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
                    audioUrl = URL.createObjectURL(audioBlob);
                    playButton.disabled = false;
                    audioChunks = [];
                });
            });
    }
}

function playRecording() {
    if (audioUrl) {
        const audio = new Audio(audioUrl);
        audio.play();
    }
}

function playStimulus() {
    // Implement this function to play the stimulus word audio from the server
    // You'll need to set up an endpoint on your server to serve the audio file
    console.log('Playing stimulus audio');
}