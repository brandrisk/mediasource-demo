<template>
    <div class="container">
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
}
</style>