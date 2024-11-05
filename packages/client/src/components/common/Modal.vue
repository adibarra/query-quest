<!--
  @author: adibarra (Alec Ibarra)
  @description: This component is used to display a generic modal dialog.
-->

<script setup lang="ts">
const modelValue = defineModel<boolean>()

function close() {
  modelValue.value = false
}
</script>

<template>
  <Teleport to="body">
    <div
      v-if="modelValue"
      absolute left-0 top-0 z-999 h-full w-full flex items-center justify-center bg-black bg-opacity-50 p-2
      @click="close"
    >
      <div
        h-fit max-h-full max-w-full w-fit qq-outline bg--c-secondary p-4
        @click.stop
      >
        <slot name="header" />
        <slot name="content" />
        <slot name="footer" :close="close">
          <div flex flex-justify-end>
            <button
              qq-outline p-1 px-2 qq-hover
              @click="close"
            >
              <span mx-2>Close</span>
            </button>
          </div>
        </slot>
      </div>
    </div>
  </Teleport>
</template>
