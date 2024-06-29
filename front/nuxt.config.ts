// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  devtools: { enabled: false },
  css: [
    '~/assets/css/style.css'
  ],
  runtimeConfig: {
    public: {
      serverUrl: 'http://127.0.0.1:5000'
    }
  }
})
