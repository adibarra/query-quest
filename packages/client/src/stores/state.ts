/**
 * @author: adibarra (Alec Ibarra)
 * @description: Pinia store for handling sidebar state
 */

import { acceptHMRUpdate, defineStore } from 'pinia'

export const useStateStore = defineStore('state', () => {
  interface UserState{
    uuid: string
    username: string
  }
  const user = useStorage<UserState>('state-user',{
    uuid: '',
    username: '',
  })

  // TODO: remove always true
  const isAuthenticated = computed(() => user.value !== null || true)

  return {
    user,
    isAuthenticated,

  }
  
})

if (import.meta.hot)
  import.meta.hot.accept(acceptHMRUpdate(useStateStore as any, import.meta.hot))
