<!--
  @author: adibarra (Alec Ibarra)
  @description: This component is used to display the login/register page of the application.
-->

<script setup lang="ts">
const quest = useAPI()
const router = useRouter()
const state = useStateStore()
const activeForm = useStorage<'login' | 'register'>('query-quest/login/last-form', 'register')
const rememberMe = useStorage('query-quest/login/remember-me', false)
const username = useStorage('query-quest/login/username', '')
const password = ref('')
const confirmPassword = ref('')
const error = ref('')

useHead({
  title: `Login/Register • QueryQuest`,
})

async function handleSubmit() {
  if (activeForm.value === 'login') {
    if (!username.value || !password.value) {
      error.value = 'Please fill out all fields.'
      return
    }

    const response = await quest.auth({
      username: username.value,
      password: password.value,
    })

    if (response.code !== API_STATUS.CREATED) {
      switch (response.code) {
        case API_STATUS.NOT_FOUND:
          error.value = 'User not found.'
          break
        case API_STATUS.FORBIDDEN:
          error.value = 'Invalid password.'
          break
        default:
          error.value = response.message
          break
      }
    }
  }
  else {
    if (!username.value || !password.value || !confirmPassword.value) {
      error.value = 'Please fill out all fields.'
      return
    }

    if (password.value !== confirmPassword.value) {
      error.value = 'Passwords do not match.'
      return
    }

    const userResponse = await quest.createUser({
      username: username.value,
      password: password.value,
    })

    if (userResponse.code !== API_STATUS.CREATED) {
      switch (userResponse.code) {
        case API_STATUS.CONFLICT:
          error.value = 'Username already exists.'
          break
        default:
          error.value = userResponse.message
          break
      }
    }

    await quest.auth({
      username: username.value,
      password: password.value,
    })
  }
}

function toggleForm() {
  activeForm.value = activeForm.value === 'login' ? 'register' : 'login'

  if (activeForm.value === 'register')
    confirmPassword.value = ''
}

watch(() => state.isAuthenticated, (auth) => {
  auth && router.push('/dashboard')
}, { immediate: true })
</script>

<template>
  <div h-15svh />

  <!-- Login and Registration Forms -->
  <div flex flex-col justify-center>
    <!-- Form Container -->
    <div mx-auto mb-5 max-w-150 min-w-80 w-90svw flex flex-col gap-5 qq-outline bg--c-secondary px-8 py-8>
      <!-- Form Title -->
      <div mb-5 text-center text-3xl>
        {{ activeForm === 'login' ? 'Login' : 'Register' }}
      </div>

      <!-- Username Input -->
      <div>
        <div qq-outline qq-hover>
          <n-input-group>
            <n-input-group-label class="w-17%" min-w-fit>
              Username
            </n-input-group-label>
            <n-input
              v-model:value="username"
              placeholder="Username"
              :status="username.length >= 3 || username.length === 0 ? undefined : 'error'"
              :maxlength="20"
              autocomplete="username"
              type="text"
            />
          </n-input-group>
        </div>

        <!-- Username Requirements (Only for Registration) -->
        <div v-if="activeForm === 'register'">
          <div px-2 py-1 op-75>
            Username must be at least 3 characters long.
          </div>
        </div>
      </div>

      <!-- Password Input -->
      <div qq-outline qq-hover>
        <n-input-group>
          <n-input-group-label class="w-17%" min-w-fit>
            Password
          </n-input-group-label>
          <n-input
            v-model:value="password"
            placeholder="Password"
            :status="password.length >= 6 || password.length === 0 ? undefined : 'error'"
            :autocomplete="activeForm === 'register' ? 'new-password' : 'current-password'"
            type="password"
            show-password-on="click"
            @keypress.enter="handleSubmit"
          />
        </n-input-group>
      </div>

      <!-- Confirm Password Input (Only for Registration) -->
      <div
        v-if="activeForm === 'register'"
        mb-3
      >
        <div qq-outline qq-hover>
          <n-input-group>
            <n-input-group-label class="w-17%" min-w-fit>
              Confirm Password
            </n-input-group-label>
            <n-input
              v-model:value="confirmPassword"
              placeholder="Confirm Password"
              :status="password === confirmPassword ? 'success' : 'error'"
              autocomplete="new-password"
              type="password"
              show-password-on="click"
              @keypress.enter="handleSubmit"
            />
          </n-input-group>
        </div>
        <div px-2 py-1 op-75>
          Password must be at least 6 characters long.
        </div>
      </div>

      <!-- Remember and Forgot password (Only for Login) -->
      <div
        v-if="activeForm === 'login'"
        flex items-center justify-between
      >
        <n-checkbox v-model:checked="rememberMe">
          Remember Me
        </n-checkbox>
        <!-- forgot password link commented out for now
        <router-link to="/forgot-password" qq-link>
          Forgot Password?
        </router-link>
        -->
      </div>

      <!-- Error Message -->
      <div v-if="error" text-red>
        {{ error }}
      </div>

      <!-- Submit Button -->
      <button
        mt-5 qq-outline bg--c-inverse hover:bg--c-accent px-2 py-0.5 text-lg text--c-primary
        @click="handleSubmit"
      >
        {{ activeForm === 'login' ? 'Sign In' : 'Create Account' }}
      </button>

      <!-- Redirect Link -->
      <span flex flex-row items-center justify-center gap-2 text-lg>
        {{ activeForm === 'login' ? 'No account?' : 'Already have an account?' }}
        <a
          cursor-pointer qq-link
          @click="toggleForm"
        >
          {{ activeForm === 'login' ? 'Sign Up' : 'Sign In' }}
        </a>
      </span>
    </div>
  </div>
</template>

<style>
.n-input .n-input__state-border {
  display: none !important;
}
</style>

<route lang="yaml">
  meta:
    layout: default
</route>
