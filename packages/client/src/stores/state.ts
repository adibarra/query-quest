/**
 * @author: adibarra (Alec Ibarra)
 * @description: Pinia store for handling sidebar state
 */

import { acceptHMRUpdate, defineStore } from 'pinia'
import type { User } from '~/types'

const quest = useAPI()

export const useStateStore = defineStore('state', () => {
  const isAuthenticated = computed(() => quest.getToken().length > 0)
  const user = ref<User | null>(null)

  watch(isAuthenticated, async () => {
    if (!isAuthenticated.value) return null

    const response = await quest.getUser()
    if (response.code === API_STATUS.OK) {
      return response.data
    }
    return null
  }, { immediate: true })

  return {
    user,
    isAuthenticated,
  }
})

if (import.meta.hot)
  import.meta.hot.accept(acceptHMRUpdate(useStateStore as any, import.meta.hot))
