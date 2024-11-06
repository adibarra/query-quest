<!--
  @author: adibarra (Alec Ibarra)
  @description: This component is used to display the 404 page of the application.
-->

<script setup lang="ts">
useHead({
  title: `Not Found • QueryQuest`,
  meta: [
    { name: 'robots', content: 'noindex, nofollow' },
  ],
})
</script>

<template>
  <div h-20svh />
  <div mx-auto w-fit rd-2 p-5 outline-1 outline>
    <div text-4xl font-900>
      <span text-red>404:</span>
      Not Found
    </div>
    <button
      title="Go Back"
      mt-2 flex text-lg qq-icon-btn
      @click="$router.back()"
      @keydown.enter="$router.back()"
    >
      <div i-carbon:caret-left text-2xl />
      Go Back
    </button>
  </div>
  <div grow />
</template>

<route lang="yaml">
  meta:
    layout: dashboard
</route>
