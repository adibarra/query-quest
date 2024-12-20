<!--
  @author: adibarra (Alec Ibarra)
  @description: This component is used to display the home page of the application.
-->

<script setup lang="ts">
import type { Question, Tag } from '~/types'

useHead({
  title: `Dashboard • QueryQuest`,
})

const router = useRouter()
const quest = useAPI()

const loading = ref(true)
const allQuestions = ref<Question[]>([])
const allTags = ref<Tag[]>([])
const tagOptions = computed(() => allTags.value.map(tag => ({ label: tag.name, value: tag.id })))

const tagQuery = ref<number[]>([])
const filteredQuestions = computed(() => {
  if (tagQuery.value.length === 0)
    return allQuestions.value
  return allQuestions.value.filter(question => tagQuery.value.every(tag => question.tags.includes(tag)))
})

function goToPlayPage(questionId: number) {
  router.push({
    path: '/dashboard/play',
    query: { id: questionId },
  })
}

function loadRandomQuestion() {
  const randomIndex = Math.floor(Math.random() * allQuestions.value.length) + 1
  goToPlayPage(allQuestions.value[randomIndex].id)
}

onMounted(async () => {
  quest.getTags().then((response) => {
    if (response.code === API_STATUS.OK) {
      allTags.value = response.data
    }
  })

  quest.getQuestions().then((response) => {
    if (response.code === API_STATUS.OK) {
      allQuestions.value = response.data
    }
    loading.value = false
  })
})
</script>

<template>
  <main h-full w-full flex flex-col gap-2>
    <span mb-3 text-3xl>
      Trivia Questions
    </span>

    <div flex flex-row justify-between gap-2>
      <div max-w-md w-full flex flex-col gap-2>
        <label text--c-inverse font-medium>
          Search by tags:
        </label>
        <NSelect
          placeholder="Select or type tags"
          clearable filterable multiple
          :options="tagOptions"
          @update:value="(value: number[]) => tagQuery = value"
        />
      </div>

      <NButton
        type="primary"
        size="medium"
        mt-auto max-w-100 bg--c-secondary text--c-inverse
        @click="loadRandomQuestion"
      >
        Play Random Question
      </NButton>
    </div>

    <div mt-2 flex grow flex-col>
      <div v-if="loading" flex grow justify-center>
        <n-spin size="large" />
      </div>

      <div v-else-if="filteredQuestions.length" flex flex-wrap gap-x4>
        <NCard
          v-for="question in filteredQuestions"
          :key="question.id"
          :title="question.question"
          mb-4 rounded-md bg--c-secondary p-2 shadow-md
        >
          <div mt-auto h-full w-full flex flex-row justify-between>
            <div flex flex-col gap-2>
              <div mt-auto flex>
                <span>Difficulty:</span>
                <NRate :default-value="question.difficulty" readonly />
              </div>

              <div flex gap-2>
                <span>Tags:</span>
                <div flex gap-1>
                  <NTag
                    v-for="tagID in question.tags"
                    :key="tagID"
                    type="success"
                    size="small"
                  >
                    {{ allTags.find((tag: Tag) => tag.id === tagID)?.name }}
                  </NTag>
                </div>
              </div>
            </div>

            <NButton
              type="primary"
              size="medium"
              mt-auto bg--c-primary text--c-inverse
              @click="goToPlayPage(question.id)"
            >
              Play
            </NButton>
          </div>
        </NCard>
      </div>

      <div v-else-if="tagQuery">
        <span text-red font-600>
          No questions found with all selected tags.
        </span>
      </div>
    </div>
  </main>
</template>

<route lang="yaml">
  meta:
    layout: dashboard
</route>
