<!--
  @author: adibarra (Alec Ibarra)
  @description: This component is used to create a new trivia question.
-->

<script setup lang="ts">
import { useMessage } from 'naive-ui'
import type { Tag } from '~/types'

const message = useMessage()
const router = useRouter()
const quest = useAPI()

const question = ref('')
const options = ref(['', ''])
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

async function handleSubmit() {
  if (question.value === '') {
    message.error('You must provide a question')
    return
  }

  if (options.value.length < 2) {
    message.error('You must provide at least 2 options')
    return
  }

  if (options.value[0] === '' || options.value[1] === '') {
    message.error('All options must be filled out')
    return
  }

  const response = await quest.createQuestion({
    question: question.value,
    difficulty: difficulty.value,
    options: options.value,
    tags: tags.value,
  })

  if (response.code === API_STATUS.CREATED) {
    message.success('Question created successfully!')
    clearForm()
  }
  else {
    message.error('Failed to create question')
  }
}

function handleCancel() {
  router.push('/dashboard')
}

function clearForm() {
  question.value = ''
  options.value = ['', '']
  difficulty.value = 1
  tags.value = []
}

function addOptions() {
  if (options.value.length < 4) {
    options.value.push('')
  }
}

function removeOption(index: number) {
  if (options.value.length > 2) {
    options.value.splice(index, 1)
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
        <div v-for="(_, index) in options" :key="index" class="mb-2 w-full flex flex-row items-center gap-2">
          <n-input
            v-model:value="options[index]"
            :placeholder="`Option ${index + 1}`"
            maxlength="50"
            show-count
          />
          <n-button
            v-if="options.length > 2"
            @click="removeOption(index)"
          >
            -
          </n-button>
          <n-button
            v-if="options.length < 4 && index === options.length - 1"
            @click="addOptions"
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
