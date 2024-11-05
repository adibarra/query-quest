<!--
  @author: adibarra (Alec Ibarra)
  @description: This component is used to display the sidebar at the left of the application.
-->

<script setup lang="ts">
import type { MenuInst, MenuOption } from 'naive-ui'
import {
  Add as AddIcon,
  Analytics as AnalyticsIcon,
  Dashboard as DashboardIcon,
  User as UserIcon,
} from '@vicons/carbon'
import { NIcon } from 'naive-ui'

const route = useRoute()
const store = useSidebarStore()
const menuOptions1: MenuOption[] = [
  { label: 'Dashboard', key: '/dashboard', icon: renderIcon(DashboardIcon) },
  { label: 'Create', key: '/dashboard/create', icon: renderIcon(AddIcon) },
  { label: 'Stats', key: '/dashboard/stats', icon: renderIcon(AnalyticsIcon) },
]

const menuOptions2: MenuOption[] = [
  { key: 'divider-1', type: 'divider' },
  { label: 'Account', key: '/dashboard/account', icon: renderIcon(UserIcon) },
]

function renderIcon(icon: Component) {
  return () => h(NIcon, null, { default: () => h(icon) })
}

const menu1SelectedKey = ref('')
const menu2SelectedKey = ref('')
const menu1 = ref<MenuInst | null>(null)
const menu2 = ref<MenuInst | null>(null)
function selectAndExpand(key: string) {
  menu1SelectedKey.value = key
  menu2SelectedKey.value = key
  menu1.value?.showOption(key)
  menu2.value?.showOption(key)
}

watch(() => route.path, () => {
  selectAndExpand(route.path)
}, { immediate: true })
</script>

<template>
  <n-layout-sider
    :width="220"
    :collapsed="store.collapsed"
    collapse-mode="width"
    show-trigger="bar"
    bordered
    @update:collapsed="store.toggle"
  >
    <div h-full flex flex-col>
      <n-scrollbar>
        <n-menu
          ref="menu1"
          v-model:value="menu1SelectedKey"
          :options="menuOptions1"
          @update:value="(key: string) => {
            $router.push(key)
          }"
        />
      </n-scrollbar>
      <div h-fit>
        <n-menu
          ref="menu2"
          v-model:value="menu2SelectedKey"
          :options="menuOptions2"
          @update:value="(key: string) => {
            $router.push(key)
          }"
        />
      </div>
    </div>
  </n-layout-sider>
</template>
