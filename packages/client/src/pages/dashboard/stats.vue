<!--
  @author: adibarra (Alec Ibarra)
  @description: This component is used to change user account information.
-->

<script setup lang="ts">
useHead({
  title: `Stats • QueryQuest`,
})

const state = useStateStore()

onMounted(async () => {
  state.refreshStats()
})
</script>

<template>
  <main h-full w-full flex flex-col gap-2>
    <span mb-3 text-3xl>
      Statistics
    </span>

    <div v-if="state.stats" div flex flex-col>
      <span px-2 py-1 op-75>
        Total Wins: {{ state.stats.wins }}
      </span>
      <span px-2 py-1 op-75>
        Total Losses: {{ state.stats.losses }}
      </span>
      <span px-2 py-1 op-75>
        Experience Points: {{ state.stats.xp }}
      </span>
    </div>
    <div v-else>
      <span px-2 py-1 op-75>
        Loading...
      </span>
    </div>
  </main>
</template>

<route lang="yaml">
  meta:
    layout: dashboard
</route>
