<!--
  @author: adibarra (Alec Ibarra)
  @description: This component is used to display the home page of the application.
-->

<script setup lang="ts">
const commitHash = import.meta.env.VITE_COMMIT_HASH

useHead({
  title: `Main • QueryQuest`,
})
</script>

<template>
  <main flex grow flex-col px-4>
    <div h-10svh />
    <div mx-2svw flex flex-col gap-2>
      Temporary links while in development
      <RouterLink to="/login">
        <n-button>
          To Login Page
        </n-button>
      </RouterLink>
    </div>
  </main>
  <span
    :class="isMobile ? 'left-8' : 'left-1'"
    absolute bottom-0.5 text-sm op-5
  >
    {{ commitHash }}
  </span>
</template>

<route lang="yaml">
  meta:
    layout: default
</route>
