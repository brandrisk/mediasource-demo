<template>
    <div v-if="props.filename">
        <div id="overlay" @click="playOrPause" class="debug"></div>
        <video controls autoplay @loadedmetadata="fitOverlay" id="video" ref="video" :src="src"
            :width="props.width"></video>
    </div>
    <div v-else id="placeholder" :style="{ width: `${props.width}px` }">No video</div>
</template>

<script setup>
const props = defineProps({
    filename: String,
    width: {
        type: Number,
        default: 400
    }
});

const serverURL = 'http://127.0.0.1:5000';
const video = ref(null);
const src = ref('');

watch(src, fitOverlay);

window.addEventListener('resize', fitOverlay);

function playOrPause() {
    if (video.value.paused) {
        video.value.play();
    } else {
        video.value.pause();
    }
}

onMounted(async () => {
    const videoURL = `${serverURL}/video/${props.filename}`;
    
    const res = await fetch(`${serverURL}/codecs/${props.filename}`);
    const codecs = await res.text();
    const mimeCodec = `video/mp4; codecs="${codecs}"`;
    
    if ('MediaSource' in window && MediaSource.isTypeSupported(mimeCodec)) {
        const mediaSource = new MediaSource;
        src.value = URL.createObjectURL(mediaSource);
        mediaSource.addEventListener('sourceopen', sourceOpen);
    } else {
        console.error('Unsupported MIME type or codec: ', mimeCodec);
    }
    
    function sourceOpen(_) {
        const mediaSource = this;
        const sourceBuffer = mediaSource.addSourceBuffer(mimeCodec);
        
        fetchAB(videoURL, function (buf) {
            sourceBuffer.addEventListener('updateend', function (_) {
                mediaSource.endOfStream();
            });
            
            sourceBuffer.appendBuffer(buf);
        });
    }
    
    function fetchAB(url, cb) {
        fetch(url).then(res => res.arrayBuffer()).then(ab => cb(ab));
    }
});

function fitOverlay() {
    try {
        const overlay = document.querySelector('#overlay');
        const vid = document.querySelector('#video');
        const rect = vid.getBoundingClientRect();

        overlay.style.width = `${rect.width}px`;
        overlay.style.height = `${rect.height}px`;
        overlay.style.left = `${rect.left}`;
        overlay.style.top = `${rect.top}`;
    } catch (e) {

    }
}
</script>

<style scoped>
.debug {
    border: 1px solid red;
}

#video {
    aspect-ratio: 16/9;
}

#overlay {
    position: absolute;
    z-index: 10;
    display: flex;
    align-items: flex-end;
    flex-direction: column;

    display: none;
}

#placeholder {
    display: flex;
    justify-content: center;
    align-items: center;
    aspect-ratio: 16/9;
    background: black;
    box-shadow: 0 0 20px white inset;
}
</style>