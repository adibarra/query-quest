<script setup lang="ts">
import PullToRefresh from 'pulltorefreshjs'

onMounted(() => {
  const iosPWA = ((navigator as any).standalone === true)
  if (!iosPWA)
    return

  PullToRefresh.init({
    mainElement: 'body',
    onRefresh() {
      window.location.reload()
    },
  })
})
</script>

<template>
  <div />
</template>

<style>
.ptr--text {
  color: var(--c-text) !important;
}
.ptr--icon {
  color: var(--c-text) !important;
}
</style>
