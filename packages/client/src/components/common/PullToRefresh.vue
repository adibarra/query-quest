<!--
  @author: adibarra (Alec Ibarra)
  @description: This component is used to enable pull-to-refresh functionality on iOS PWAs.
-->

<script setup lang="ts">
onMounted(async () => {
  const iosPWA = ((navigator as any).standalone === true)
  if (!iosPWA)
    return

  const { default: PullToRefresh } = await import('pulltorefreshjs')

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
