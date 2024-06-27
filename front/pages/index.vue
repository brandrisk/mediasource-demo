<template>
    <div id="container">
        <input id="fileInput" ref="fileInput" type="file" @change="upload" accept="video/mp4">
        <div class="button" @click="openFilePicker">Upload</div>
        <div v-if="err">Something went wrong</div>
        <NuxtLink v-if="filename" :to="`/video/${filename}`">Open video</NuxtLink>
        <div v-if="vids.length != 0" v-for="vid in vids">
            <NuxtLink :to="`/video/${vid}`">{{ vid }}</NuxtLink>
        </div>
    </div>
  </template>
  
<script setup>
  const serverURL = 'http://127.0.0.1:5000';
  const fileInput = ref(null);
  const uploaded = ref(false);
  const file = ref(null);
  const filename = ref('');
  const err = ref(false);
  const vids = ref([]);

  onMounted(async () => {
    const res = await fetch(`${serverURL}/list`);
    vids.value = await res.json();
  });
  
  function openFilePicker() {
    fileInput.value.click();
  }

  async function upload() {
    file.value = fileInput.value.files[0];
  
    const data = new FormData();
    data.append('video', file.value);
  
    try {
        const res = await fetch(
            `${serverURL}/upload`, {
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
  }
  
  </script>
  
  <style scoped>
  .button {
    background: black;
    color: white;
    border-radius: 5px;
    padding: 10px;
    width: fit-content;
    cursor: pointer;
    border: 2px solid white;
  }
  
  .button:hover {
    box-shadow: 0 0 10px white inset;
  }
  
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
  