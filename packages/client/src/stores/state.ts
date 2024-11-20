/**
 * @author: adibarra (Alec Ibarra)
 * @description: Pinia store for handling sidebar state
 */

import { acceptHMRUpdate, defineStore } from 'pinia'
import type { Stats, User } from '~/types'

const quest = useAPI()

export const useStateStore = defineStore('state', () => {
  const isAuthenticated = computed(() => !!quest.getSession())
  const user = ref<User | null>(null)
  const stats = ref<Stats | null>(null)

  async function refreshUser() {
    if (isAuthenticated.value) {
      const uuid = quest.getSession()!.user_uuid
      const response = await quest.getUser({ uuid })
      if (response.code === API_STATUS.OK) {
        user.value = response.data
        return
      }
    }
    user.value = null
    await quest.deauth()
  }

  async function refreshStats() {
    if (isAuthenticated.value) {
      const response = await quest.getStats()
      if (response.code === API_STATUS.OK) {
        stats.value = response.data
        return
      }
    }
    stats.value = null
  }

  watch(isAuthenticated, async () => {
    await refreshUser()
    await refreshStats()
  }, { immediate: true })

  return {
    isAuthenticated,
    user,
    stats,
    refreshUser,
    refreshStats,
  }
})

if (import.meta.hot)
  import.meta.hot.accept(acceptHMRUpdate(useStateStore as any, import.meta.hot))
