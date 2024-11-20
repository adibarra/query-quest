<!--
  @author: adibarra (Alec Ibarra)
  @description: This component is used to display the change username modal.
-->

<script setup lang="ts">
import { useMessage } from 'naive-ui'

const isOpen = defineModel<boolean>()

const quest = useAPI()
const state = useStateStore()
const message = useMessage()

const username = ref('')
const error = ref('')

async function changeUsername(slotCloseFunc: any) {
  if (username.value.length < 3) {
    error.value = 'Username must be at least 3 characters long.'
    return
  }

  const response = await quest.updateUser({ username: username.value })
  if (response.code === API_STATUS.OK) {
    state.refreshUser()
    message.success('Username changed successfully')
    close(slotCloseFunc)
    return
  }

  message.error('Failed to change username')
  switch (response.code) {
    case API_STATUS.BAD_REQUEST:
      error.value = 'Your username is invalid.'
      break
    default:
      error.value = 'An error occurred. Try again later.'
  }
}

function close(slotCloseFunc: any) {
  username.value = ''
  error.value = ''
  isOpen.value = false
  slotCloseFunc()
}
</script>

<template>
  <Modal v-model="isOpen">
    <template #header>
      <span ml-2 text-3xl>Change Username</span>
    </template>
    <template #content>
      <div mx-auto max-w-100 min-w-50 w-80svw flex flex-col gap-5 px-8 py-8>
        <div>
          <div qq-outline qq-hover>
            <n-input-group>
              <n-input-group-label class="w-17%" min-w-fit>
                New Username
              </n-input-group-label>
              <n-input
                v-model:value="username"
                placeholder="New Username"
                :status="username.length >= 3 || username.length === 0 ? undefined : 'error'"
                autocomplete="new-username"
              />
            </n-input-group>
          </div>
          <div px-2 py-1 op-75>
            Username must be at least 3 characters long.
          </div>
        </div>
        <div v-if="error" px-2 py-1 text-red>
          {{ error }}
        </div>
      </div>
    </template>
    <template #footer="footerProps">
      <div flex gap-2 flex-justify-end>
        <button
          qq-outline px-2 py-0.5 text-lg qq-hover
          @click="close(footerProps.close)"
        >
          <span mx-2>Cancel</span>
        </button>
        <button
          qq-outline bg--c-inverse hover:bg--c-accent px-2 py-0.5 text-lg text--c-primary
          @click="changeUsername(footerProps.close)"
        >
          <span mx-2>Save</span>
        </button>
      </div>
    </template>
  </Modal>
</template>

<style>
.n-input .n-input__state-border {
  display: none !important;
}
</style>
