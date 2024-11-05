<!--
  @author: adibarra (Alec Ibarra)
  @description: This component is used to render user account information.
-->

<script setup lang="ts">
useHead({
  title: `Account • QueryQuest`,
})

const usernameModal = ref(false)
const passwordModal = ref(false)
</script>

<template>
  <main mx-auto flex grow flex-col px-4>
    <div h-10svh />

    <div mx-2svw mb-2 max-w-150 w-80svw flex flex-col gap-2>
      <span text-3xl>
        Account
      </span>

      <div flex justify-between>
        <div flex flex-col gap-2>
          <n-button
            @click="usernameModal = true"
          >
            Change Username
          </n-button>
          <n-button
            @click="passwordModal = true"
          >
            Change Password
          </n-button>
        </div>
      </div>
   </div>

    <ChangeUsernameModal v-model="usernameModal" />
    <ChangePasswordModal v-model="passwordModal" />
  </main>
</template>

<route lang="yaml">
  meta:
    layout: dashboard
</route>
