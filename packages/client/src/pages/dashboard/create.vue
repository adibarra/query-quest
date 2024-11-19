<!--
  @author: adibarra (Alec Ibarra)
  @description: This component is used to create a new trivia question.
-->

<script setup lang="ts">
import type { Tag } from '~/types'

const router = useRouter()
const quest = useAPI()

const question = ref('')
const answers = ref(['', ''])
const difficulty = ref(1)
const tags = ref<number[]>([])

const allTags = ref<Tag[]>([
  { id: 1, name: 'Geography', description: '' },
  { id: 2, name: 'Science', description: '' },
  { id: 3, name: 'History', description: '' },
  { id: 4, name: 'Literature', description: '' },
  { id: 5, name: 'Mathematics', description: '' },
  { id: 6, name: 'Art & Culture', description: '' },
  { id: 7, name: 'Technology', description: '' },
  { id: 8, name: 'Nature', description: '' },
  { id: 9, name: 'Space', description: '' },
  { id: 10, name: 'General', description: '' },
])
const tagOptions = computed(() => allTags.value.map(tag => ({ label: tag.name, value: tag.id })))

useHead({
  title: `Create • QueryQuest`,
})

function handleSubmit() { }

function handleCancel() {
  router.push('/dashboard')
}

function addAnswer() {
  if (answers.value.length < 4) {
    answers.value.push('')
  }
}

function removeAnswer(index: number) {
  if (answers.value.length > 2) {
    answers.value.splice(index, 1)
  }
}
</script>

<template>
  <main h-full max-w-150 w-full flex flex-col gap-2>
    <span mb-3 text-3xl>
      Create Trivia Question
    </span>

    <div mb-2>
      <div flex flex-col>
        <span text-lg>
          Question
        </span>
        <span px-2 py-1 op-75>
          This should be a question that can be answered with one of the provided options.
        </span>
      </div>
      <n-input
        v-model:value="question"
        placeholder="Enter your question"
        type="textarea"
        maxlength="500"
        show-count
      />
    </div>

    <div mb-2>
      <div flex flex-col>
        <span text-lg>
          Options
        </span>
        <span px-2 py-1 op-75>
          The first option should be the correct answer. You can have from 2 to 4 options.
        </span>
      </div>
      <div w-full flex flex-col>
        <div v-for="(_, index) in answers" :key="index" class="mb-2 w-full flex flex-row items-center gap-2">
          <n-input
            v-model:value="answers[index]"
            :placeholder="`Option ${index + 1}`"
            maxlength="50"
            show-count
          />
          <n-button
            v-if="answers.length > 2"
            @click="removeAnswer(index)"
          >
            -
          </n-button>
          <n-button
            v-if="answers.length < 4 && index === answers.length - 1"
            @click="addAnswer"
          >
            +
          </n-button>
        </div>
      </div>
    </div>

    <div mb-2>
      <div flex flex-col>
        <span text-lg>
          Difficulty
        </span>
        <span px-2 py-1 op-75>
          Select the difficulty of the question.
        </span>
      </div>
      <n-rate
        v-model:value="difficulty"
        :count="5"
      />
    </div>

    <div mb-2>
      <div flex flex-col>
        <span text-lg>
          Tags
        </span>
        <span px-2 py-1 op-75>
          Select the tags that best describe the question.
        </span>
      </div>
      <n-select
        v-model:value="tags"
        :options="tagOptions"
        placeholder="Select tags"
        multiple
      />
    </div>

    <div mt-2 flex gap-2>
      <n-button
        qq-hover
        @click="handleCancel"
      >
        Cancel
      </n-button>
      <n-button
        type="primary"
        bg--c-inverse qq-hover
        @click="handleSubmit"
      >
        Submit
      </n-button>
    </div>
  </main>
</template>

<style>
.n-input .n-input__state-border {
  display: none !important;
}
</style>

<route lang="yaml">
  meta:
    layout: dashboard
</route>
