<template>
    <div id="container">
        <input id="fileInput" ref="fileInput" type="file" @change="upload" accept="video/mp4">
        <div class="button" @click="openFilePicker">Upload</div>
        <div v-if="err">Something went wrong</div>
        <div v-if="processing">Processing...</div>
        <br>
        <div v-if="vids.length != 0" v-for="vid in vids">
            <NuxtLink :to="`/video/${vid}`">{{ vid }}</NuxtLink>
        </div>
    </div>
</template>

<script setup>
const config = useRuntimeConfig();
const serverUrl = config.public.serverUrl;

const fileInput = ref(null);
const uploaded = ref(false);
const file = ref(null);
const filename = ref('');
const err = ref(false);
const vids = ref([]);
const processing = ref(false);

onMounted(async () => {
    const res = await fetch(`${serverUrl}/list`);
    vids.value = await res.json();
});

function openFilePicker() {
    fileInput.value.click();
}

async function upload() {
    file.value = fileInput.value.files[0];
    
    const data = new FormData();
    data.append('video', file.value);
    processing.value = true;

    try {
        const res = await fetch(
            `${serverUrl}/upload`, {
            method: 'post',
            body: data,
        });

        filename.value = await res.text();
        uploaded.value = true;

        if (!filename.value) {
            err.value = true;
        }
    } catch (e) {
        console.error(e)
    }

    processing.value = false;
    vids.value.push(filename.value);
}

</script>

<style scoped>
#fileInput {
    display: none;
}

#container {
    display: flex;
    justify-content: center;
    align-items: center;
    flex-direction: column;
    gap: 10px;
    padding: 10px 0;
}
</style>