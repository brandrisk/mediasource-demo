<template>
    <div class="container">
        <NuxtLink class="button" to="/">Home</NuxtLink>

        <ClientOnly>
            <Player :filename="route.params.filename" :width="700"></Player>
        </ClientOnly>
    </div>
</template>


<script setup>
const route = useRoute();

</script>


<style scoped>
.container {
    margin: auto;
    display: flex;
    justify-content: center;
    align-items: center;
    flex-direction: column;
    gap: 10px;
    padding: 10px 0;
}
</style>