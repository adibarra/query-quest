/**
 * @author: adibarra (Alec Ibarra)
 * @description: Pinia store for handling sidebar state
 */

import { acceptHMRUpdate, defineStore } from 'pinia'
import type { User } from '~/types'

export const useStateStore = defineStore('state', () => {
  const user = ref<User | null>(null)

  // TODO: remove always true
  const isAuthenticated = computed(() => user.value !== null || true)

  return {
    user,
    isAuthenticated,
  }
})

if (import.meta.hot)
  import.meta.hot.accept(acceptHMRUpdate(useStateStore as any, import.meta.hot))
