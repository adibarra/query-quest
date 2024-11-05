<!--
  @author: adibarra (Alec Ibarra)
  @description: This component is used to change user account information.
-->

<script setup lang="ts">
useHead({
  title: `Profile • QueryQuest`,
})

const xp = ref(0)
const wins = ref(0)
const losses = ref(0)
</script>

<template>
  <main mx-auto flex grow flex-col px-4>
    <div h-10svh />

    <div mx-2svw mb-2 max-w-150 w-80svw flex flex-col gap-2>
      <span text-3xl>
        Statistics
      </span>

      <div flex flex-col>
        <span px-2 py-1 op-75>
          Total Wins: {{ wins }}
        </span>
        <span px-2 py-1 op-75>
          Total Losses: {{ losses }}
        </span>
        <span px-2 py-1 op-75>
          Experience Points: {{ xp }}
        </span>
      </div>
    </div>
  </main>
</template>

<route lang="yaml">
  meta:
    layout: dashboard
</route>
