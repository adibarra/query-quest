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

const allQuestions = ref<Question[]>([])
const availableTags = ref<Tag[]>([])
const tagQuery = ref<string[]>([])
const filteredQuestions = computed(() => {
  if (tagQuery.value.length === 0)
    return allQuestions.value
  const searchTags = tagQuery.value.map(tag => tag.toLowerCase())
  return allQuestions.value.filter(question => {
    const tags = question.tags.map(tagID => availableTags.value.find(tag => tag.id === tagID)?.name.toLowerCase())
    return searchTags.every(tag => tags.includes(tag))
  })
})

function goToPlayPage(questionId: number) {
  router.push({
    path: '/dashboard/play',
    query: { id: questionId },
  })
}

function loadRandomQuestion() {
  const randomIndex = Math.floor(Math.random() * allQuestions.value.length)
  const randomQuestion = allQuestions.value[randomIndex]
  goToPlayPage(randomQuestion.id)
}

onMounted(async () => {
  const response = await quest.getQuestions()
  if (response.code === API_STATUS.OK) {
    allQuestions.value = response.data
  }
})
</script>

<template>
  <main h-full w-full flex flex-col gap-2>
    <span mb-3 text-3xl>
      Trivia Questions
    </span>

    <div flex flex-row justify-between>
      <div max-w-md w-full flex flex-col gap-2>
        <label text--c-inverse font-medium>
          Search by Tag:
        </label>
        <NSelect
          placeholder="Select or type tags"
          multiple clearable filterable
          :options="availableTags"
          @update:value="(value) => tagQuery = value"
        />
      </div>

      <NButton
        type="primary"
        size="large"
        mt-auto max-w-100 bg--c-secondary text--c-inverse
        @click="loadRandomQuestion"
      >
        Play Random Question
      </NButton>
    </div>

    <div v-if="filteredQuestions.length">
      <div mt-2 space-y-4>
        <NCard
          v-for="question in filteredQuestions"
          :key="question.id"
          :title="question.question"
          rounded-md bg--c-secondary p-2 shadow-md
        >
          <div flex flex-row justify-between>
            <div flex flex-col gap-2>
              <div flex>
                <span>Difficulty:</span>
                <NRate :default-value="question.difficulty" readonly />
              </div>

              <div flex gap-2>
                <span>Tags:</span>
                <div flex gap-1>
                  <NTag
                    v-for="tag in question.tags"
                    :key="tag"
                    type="success"
                    size="small"
                  >
                    {{ tag }}
                  </NTag>
                </div>
              </div>
            </div>

            <NButton
              type="primary"
              size="medium"
              bg--c-tertiary text--c-inverse
              @click="goToPlayPage(question.id)"
            >
              Play
            </NButton>
          </div>
        </NCard>
      </div>
    </div>

    <div v-else-if="tagQuery" mt-4>
      <p text--c-inverse italic>
        No questions found for tags: {{ tagQuery }}
      </p>
    </div>
  </main>
</template>

<route lang="yaml">
  meta:
    layout: dashboard
</route>
