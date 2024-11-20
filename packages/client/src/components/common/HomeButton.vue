<!--
  @author: adibarra (Alec Ibarra)
  @description: This component is used to display a home button.
-->

<script setup lang="ts">
import {
  Home as HomeIcon,
} from '@vicons/carbon'
</script>

<template>
  <n-tooltip>
    <template #trigger>
      <n-button
        text @click="() => {
          $router.push('/')
        }"
      >
        <n-icon size="22">
          <HomeIcon />
        </n-icon>
      </n-button>
    </template>
    Home
  </n-tooltip>
</template>
