/**
 * @author: adibarra (Alec Ibarra)
 * @description: Main entry point for the application
 */

import type { UserModule } from './types'
import { createHead } from '@unhead/vue'
import { createPinia } from 'pinia'  // 'pinia' (external) before 'vue-router' and others
import { setupLayouts } from 'virtual:generated-layouts'
import { createI18n } from 'vue-i18n'
import { createRouter, createWebHistory } from 'vue-router'
import { routes } from 'vue-router/auto-routes'
import App from './App.vue'

import '@unocss/reset/tailwind.css'
import 'uno.css'



const head = createHead()

// create the router instance
const router = createRouter({
  history: createWebHistory(),
  routes: setupLayouts(routes),
})

// Create the Vue app instance
const app = createApp(App)

// install all modules under `modules/`
Object.values(import.meta.glob<{ install: UserModule }>('./modules/*.ts', { eager: true }))
  .forEach(i => i.install?.({ app, router }))

// Install Pinia and i18n
const pinia = createPinia()
app.use(pinia)

const i18n = createI18n({
  locale: 'en',
  messages: {},
})
app.use(i18n)

// mount the app
app.use(router)
app.use(head)
app.mount('#app')
