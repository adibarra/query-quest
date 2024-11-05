<!--
  @author: adibarra (Alec Ibarra)
  @description: This component is used to display the navigation bar at the top of the application.
-->

<script setup lang="ts">
import { identicon } from '@dicebear/collection'
import { createAvatar } from '@dicebear/core'
import {
  AddOutline as AddIcon,
  NotificationsOutline as BellIcon,
  CaretDownOutline as DropdownIcon,
  LogOutOutline as LogoutIcon,
  RefreshOutline as RefreshIcon,
  PersonCircleOutline as UserIcon,
} from '@vicons/ionicons5'
import { NIcon, useMessage } from 'naive-ui'

const message = useMessage()
const route = useRoute()
const router = useRouter()

interface Crumb { label: string, key: string }
const breadcrumbs = computed(() => {
  const parts = route.path.split('/').filter(Boolean)

  let path = ''
  const crumbs: Crumb[] = parts.map((part: string) => {
    path += `/${part}`
    return {
      label: path.replaceAll('/', '.').slice(1),
      key: path,
    }
  })

  if (crumbs.length === 1)
    crumbs.push({ label: 'home', key: crumbs[0].key })

  return crumbs
})

const username = 'example'

const avatar = computed(() => {
  return createAvatar(identicon, { seed: username }).toDataUri()
})

function renderIcon(icon: Component) {
  return () => {
    return h(NIcon, null, {
      default: () => h(icon),
    })
  }
}

const isAuthenticated = ref(true)

// redirect to login if not authenticated
watch(() => isAuthenticated, () => {
  if (!isAuthenticated.value)
    router.push('/login')
}, { immediate: true })
</script>

<template>
  <n-layout-header bordered h-48px w-full flex>
    <div flex grow items-center gap-5 py-1>
      <!-- parent should be w-55 to match sidebar size -->
      <div hidden h-full w-55 items-center justify-center md:flex>
        <Logo />
      </div>

      <!-- refresh button -->
      <n-tooltip>
        <template #trigger>
          <n-button text hidden md:block @click="$router.go(0)">
            <NIcon size="20">
              <RefreshIcon />
            </NIcon>
          </n-button>
        </template>
        Refresh Page
      </n-tooltip>

      <!-- breadcrumbs keep track of what page you are on -->
      <n-breadcrumb hidden md:block>
        <template v-for="crumb in breadcrumbs" :key="crumb">
          <n-breadcrumb-item>
            <router-link :to="crumb.key">
              {{ crumb.label }}
            </router-link>
          </n-breadcrumb-item>
        </template>
      </n-breadcrumb>

      <!-- spacer to push the rest of the items to the right -->
      <div grow />

      <!-- theme switch -->
      <ThemeSwitch />

      <!-- notifications with badge -->
      <n-tooltip>
        <template #trigger>
          <n-button text @click="() => message.info(`Clicked notifications`)">
            <n-badge dot processing>
              <NIcon size="22">
                <BellIcon />
              </NIcon>
            </n-badge>
          </n-button>
        </template>
        Notifications
      </n-tooltip>

      <!-- user dropdown -->
      <n-dropdown
        :options="[
          { key: 0, label: username, icon: renderIcon(UserIcon), disabled: true },
          { key: 1, type: 'divider' },
          { key: 2, label: 'Logout', icon: renderIcon(LogoutIcon) },
        ]"
        trigger="click"
        @select="async (key: any, option: any) => {
          if (key === 2) {
            message.success('Logged out')
            isAuthenticated.value = false
          }
        }"
      >
        <n-avatar
          size="small"
          :src="avatar"
          mr-5 cursor-pointer
        />
      </n-dropdown>
    </div>
  </n-layout-header>
</template>
