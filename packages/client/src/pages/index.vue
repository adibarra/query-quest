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
    <div mx-auto mt-20vh max-w-120 min-w-75 w-92vw sm:min-w-120>
      <div />
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
