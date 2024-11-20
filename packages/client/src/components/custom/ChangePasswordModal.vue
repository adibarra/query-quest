<!--
  @author: adibarra (Alec Ibarra)
  @description: This component is used to display the change password modal.
-->

<script setup lang="ts">
import { useMessage } from 'naive-ui'

const isOpen = defineModel<boolean>()

const quest = useAPI()
const state = useStateStore()
const message = useMessage()

const password = ref('')
const confirmPassword = ref('')
const error = ref('')

async function changePassword(slotCloseFunc: any) {
  if (password.value.length < 6) {
    error.value = 'Password must be at least 6 characters long.'
    return
  }

  if (password.value !== confirmPassword.value) {
    error.value = 'Passwords do not match.'
    return
  }

  const response = await quest.updateUser({ password: password.value })
  if (response.code === API_STATUS.OK) {
    state.refreshUser()
    message.success('Password changed successfully')
    close(slotCloseFunc)
    return
  }

  message.error('Failed to change password')
  switch (response.code) {
    case API_STATUS.BAD_REQUEST:
      error.value = 'Your password is invalid.'
      break
    default:
      error.value = 'An error occurred. Try again later.'
  }
}

function close(slotCloseFunc: any) {
  password.value = ''
  error.value = ''
  isOpen.value = false
  slotCloseFunc()
}
</script>

<template>
  <Modal v-model="isOpen">
    <template #header>
      <span ml-2 text-3xl>Change Password</span>
    </template>
    <template #content>
      <div mx-auto max-w-100 min-w-50 w-80svw flex flex-col gap-5 px-8 py-8>
        <div qq-outline qq-hover>
          <n-input-group>
            <n-input-group-label class="w-17%" min-w-fit>
              New Password
            </n-input-group-label>
            <n-input
              v-model:value="password"
              placeholder="New Password"
              :status="password.length >= 6 || password.length === 0 ? undefined : 'error'"
              autocomplete="new-password"
              type="password"
              show-password-on="click"
            />
          </n-input-group>
        </div>
        <div>
          <div qq-outline qq-hover>
            <n-input-group>
              <n-input-group-label class="w-17%" min-w-fit>
                Confirm
              </n-input-group-label>
              <n-input
                v-model:value="confirmPassword"
                placeholder="Confirm Password"
                :status="password === confirmPassword ? 'success' : 'error'"
                autocomplete="new-password"
                type="password"
                show-password-on="click"
              />
            </n-input-group>
          </div>
          <div px-2 py-1 op-75>
            Password must be at least 6 characters long.
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
          @click="changePassword(footerProps.close)"
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
