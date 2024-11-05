<!--
  @author: adibarra (Alec Ibarra)
  @description: This component is used to create a new trivia question.
-->

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const question = ref('')
const answers = ref(['', ''])
const difficulty = ref(1)
const tags = ref<string[]>([])
const availableTags = ref([
  { label: 'General', value: 'general' },
  { label: 'Science', value: 'science' },
  { label: 'Technology', value: 'technology' },
  { label: 'History', value: 'history' },
  { label: 'Geography', value: 'geography' },
  { label: 'Entertainment', value: 'entertainment' },
  { label: 'Sports', value: 'sports' },
])

useHead({
  title: `Create • QueryQuest`,
})

function handleSubmit() { }

function handleCancel() {
  router.push('/')
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
  <main flex grow flex-col px-4>
    <div h-10svh />

    <div mx-2svw mb-2 max-w-150 flex flex-col gap-2>
      <span text-3xl>
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
          <div v-for="(answer, index) in answers" :key="index" class="mb-2 w-full flex flex-row items-center gap-2">
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
          :options="availableTags"
          placeholder="Select tags"
          multiple
        />
      </div>

      <div mt-2 flex gap-2>
        <n-button
          type="primary"
          bg--c-inverse qq-hover
          @click="handleSubmit"
        >
          Submit
        </n-button>
        <n-button
          qq-hover
          @click="handleCancel"
        >
          Cancel
        </n-button>
      </div>
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
