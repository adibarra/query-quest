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
  <main h-full w-full flex flex-col gap-2>
    <span mb-3 text-3xl>
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
  </main>
</template>

<route lang="yaml">
  meta:
    layout: dashboard
</route>
