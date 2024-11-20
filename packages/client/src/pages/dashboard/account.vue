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
const deleteModal = ref(false)
</script>

<template>
  <main h-full w-full flex flex-col gap-2>
    <span mb-3 text-3xl>
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
        <n-button
          @click="deleteModal = true"
        >
          Delete Account
        </n-button>
      </div>
    </div>

    <ChangeUsernameModal v-model="usernameModal" />
    <ChangePasswordModal v-model="passwordModal" />
    <DeleteUserModal v-model="deleteModal" />
  </main>
</template>

<route lang="yaml">
  meta:
    layout: dashboard
</route>
