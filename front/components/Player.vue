<template>
    <div v-if="src">
        <div id="overlay" @click="playOrPause" class="debug"></div>
        <video @error="src = ''" controls autoplay @loadedmetadata="fitOverlay" id="video" :src="src"
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

const config = useRuntimeConfig();
const serverUrl = config.public.serverUrl;
const src = ref('');
const videoURL = ref('');
const mimeCodec = ref('');
const ms = ref(null);

watch(src, fitOverlay);

window.addEventListener('resize', fitOverlay);

function playOrPause() {
    const video = document.querySelector('#video');

    if (video.paused) {
        video.play();
    } else {
        video.pause();
    }
}

onMounted(async () => {
    videoURL.value = `${serverUrl}/video/${props.filename}`;

    try {
        const res = await fetch(`${serverUrl}/codecs/${props.filename}`);
        const codecs = await res.text();
        mimeCodec.value = `video/mp4; codecs="${codecs}"`;
        
        if ('MediaSource' in window && MediaSource.isTypeSupported(mimeCodec.value)) {
            ms.value = new MediaSource;
            src.value = URL.createObjectURL(ms.value);
            ms.value.addEventListener('sourceopen', sourceOpen);
        } else {
            console.error('Unsupported MIME type or codec: ', mimeCodec.value);
        }
    } catch(e) {
        src.value = '';
    }
});

function sourceOpen(_) {
    const mediaSource = this;
    const sourceBuffer = mediaSource.addSourceBuffer(mimeCodec.value);

    fetchAB(videoURL.value, function (buf) {
        sourceBuffer.addEventListener('updateend', function (_) {
            mediaSource.endOfStream();
        });

        sourceBuffer.appendBuffer(buf);
    });
}

function fetchAB(url, cb) {
    fetch(url).then(res => res.arrayBuffer()).then(ab => cb(ab));
}

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