<!--
  @author: adibarra (Alec Ibarra)
  @description: This component is used to display the play page of the application.
-->

<script setup lang="ts">
import type { Question } from '~/types'

useHead({
  title: `Play • QueryQuest`,
})

const router = useRouter()
const route = useRoute()
const quest = useAPI()

const randIDs = ref<number[]>([])
const question = ref<Question | null>(null)
const countdown = ref(3)
const state = ref<'waiting' | 'countdown' | 'options' | 'result'>('waiting')
const userAnswer = ref<string | null>(null)
const isCorrect = computed(() => question.value && userAnswer.value === question.value.options[0])

const scrambledOptions = computed(() => {
  if (!question.value)
    return []
  return shuffle([...question.value.options])
})

function startCountdown() {
  state.value = 'countdown'
  countdown.value = 3
  const countdownInterval = setInterval(() => {
    if (countdown.value > 1) {
      countdown.value -= 1
    }
    else {
      clearInterval(countdownInterval)
      showOptions()
    }
  }, 1000)
}

function showOptions() {
  state.value = 'options'
  userAnswer.value = null
}

function selectAnswer(answer: string) {
  userAnswer.value = answer
  state.value = 'result'

  quest.updateStats({
    correct: !!isCorrect.value,
  })
}

function getNextID() {
  const nextID = randIDs.value.pop()
  if (nextID != null)
    return nextID
  randIDs.value = shuffle([...Array.from({ length: 59 }, (_, i) => i + 1)])
  return randIDs.value.pop()!
}

function loadRandomQuestion() {
  router.push({ query: { id: getNextID().toString() } })
}

function goToDashboard() {
  router.push('/dashboard')
}

watch(() => route.query.id, async () => {
  state.value = 'waiting'
  question.value = null
  const id = Number(route.query.id) ?? 1
  const response = await quest.getQuestion({ id })
  if (response.code === API_STATUS.OK) {
    question.value = response.data[0]
  }

  state.value = 'countdown'
  startCountdown()
}, { immediate: true })
</script>

<template>
  <main h-full w-full flex flex-col items-center>
    <div h-10svh />

    <div v-if="['waiting', 'countdown'].includes(state)" flex flex-col items-center>
      <div mb-4 text-center text-2xl font-semibold>
        {{ question?.question }}
      </div>
      <div mb-4 text-2xl text--c-accent font-bold>
        Get Ready!
      </div>
      <div v-show="state === 'countdown'" mb-4 text-4xl font-bold>
        {{ countdown }}
      </div>
    </div>

    <div v-if="state === 'options'" flex flex-col items-center>
      <div mb-4 text-center text-2xl font-semibold>
        {{ question?.question }}
      </div>
      <div v-if="scrambledOptions" flex flex-wrap justify-center gap-2.5>
        <NButton
          v-for="option in scrambledOptions"
          :key="option"
          type="default"
          size="large"
          class="option-button"
          style="width: calc(50% - 1rem);"
          @click="selectAnswer(option)"
        >
          {{ option }}
        </NButton>
      </div>
    </div>

    <div v-show="state === 'result'" mt-4 text-center>
      <p :class="{ 'text-green-500': isCorrect, 'text-red-500': !isCorrect }" text-2xl font-bold>
        {{ isCorrect ? 'Correct! 🎉' : 'Oops, try again! ❌' }}
      </p>

      <div mt-2 text-xl text-blue-500>
        +{{ isCorrect ? 10 : 2 }} XP
      </div>

      <div v-if="!isCorrect" mt-2 text-xl>
        Correct Answer:
        <span text-red-500 font-semibold>
          {{ question?.options[0] }}
        </span>
      </div>

      <div mt-4 flex justify-center gap-4>
        <NButton type="default" size="large" @click="goToDashboard">
          Back to Dashboard
        </NButton>
        <NButton type="default" size="large" @click="loadRandomQuestion">
          Play Random Question
        </NButton>
      </div>
    </div>
  </main>
</template>

<style scoped>
.option-button {
  transition: transform 0.2s ease;
}
.option-button:hover {
  transform: scale(1.05);
}
</style>

<route lang="yaml">
  meta:
    layout: dashboard
</route>
