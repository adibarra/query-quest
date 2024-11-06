<!--
  @author: adibarra (Alec Ibarra)
  @description: This component is used to display the home page of the application.
-->

<script setup lang="ts">
useHead({
  title: `Dashboard • QueryQuest`,
})

const allQuestions = ref([
  {
    id: 1,
    question: 'What is the capital of France?',
    options: ['Paris', 'London', 'Berlin', 'Madrid'],
    tags: ['geography', 'countries'],
    difficulty: 2,
  },
  {
    id: 2,
    question: 'Who wrote "To Kill a Mockingbird"?',
    options: ['Harper Lee', 'Mark Twain', 'F. Scott Fitzgerald', 'Ernest Hemingway'],
    tags: ['literature', 'authors'],
    difficulty: 3,
  },
  {
    id: 3,
    question: 'What is the smallest prime number?',
    options: ['2', '0', '1', '3'],
    tags: ['math', 'numbers'],
    difficulty: 1,
  },
  {
    id: 4,
    question: 'Which planet is known as the Red Planet?',
    options: ['Mars', 'Earth', 'Jupiter', 'Venus'],
    tags: ['science', 'astronomy'],
    difficulty: 2,
  },
  {
    id: 5,
    question: 'What is the largest ocean on Earth?',
    options: ['Pacific Ocean', 'Atlantic Ocean', 'Indian Ocean', 'Arctic Ocean'],
    tags: ['geography', 'oceans'],
    difficulty: 4,
  },
  {
    id: 6,
    question: 'Who painted the Mona Lisa?',
    options: ['Leonardo da Vinci', 'Vincent van Gogh', 'Pablo Picasso', 'Claude Monet'],
    tags: ['art', 'artists'],
    difficulty: 3,
  },
  {
    id: 7,
    question: 'What is the chemical symbol for gold?',
    options: ['Au', 'Ag', 'Pb', 'Fe'],
    tags: ['science', 'chemistry'],
    difficulty: 2,
  },
  {
    id: 8,
    question: 'What is the speed of light?',
    options: ['299,792 km/s', '150,000 km/s', '100,000 km/s', '1,000,000 km/s'],
    tags: ['science', 'physics'],
    difficulty: 5,
  },
  {
    id: 9,
    question: 'Who discovered America?',
    options: ['Christopher Columbus', 'Marco Polo', 'Vasco da Gama', 'Leif Erikson'],
    tags: ['history', 'explorers'],
    difficulty: 3,
  },
  {
    id: 10,
    question: 'Which element has the atomic number 1?',
    options: ['Hydrogen', 'Oxygen', 'Carbon', 'Nitrogen'],
    tags: ['science', 'elements'],
    difficulty: 1,
  },
  {
    id: 11,
    question: 'In which year did World War II end?',
    options: ['1945', '1939', '1950', '1918'],
    tags: ['history', 'wars'],
    difficulty: 4,
  },
  {
    id: 12,
    question: 'What is the tallest mountain in the world?',
    options: ['Mount Everest', 'K2', 'Kangchenjunga', 'Mount Kilimanjaro'],
    tags: ['geography', 'mountains'],
    difficulty: 3,
  },
  {
    id: 13,
    question: 'Which country is known as the Land of the Rising Sun?',
    options: ['Japan', 'China', 'South Korea', 'Vietnam'],
    tags: ['geography', 'countries'],
    difficulty: 2,
  },
  {
    id: 14,
    question: 'What is the main ingredient in guacamole?',
    options: ['Avocado', 'Tomato', 'Onion', 'Garlic'],
    tags: ['food', 'cooking'],
    difficulty: 1,
  },
  {
    id: 15,
    question: 'What is the chemical symbol for water?',
    options: ['H2O', 'O2', 'CO2', 'H2O2'],
    tags: ['science', 'chemistry'],
    difficulty: 2,
  },
  {
    id: 16,
    question: 'Who was the first President of the United States?',
    options: ['George Washington', 'Abraham Lincoln', 'Thomas Jefferson', 'John Adams'],
    tags: ['history', 'USA'],
    difficulty: 3,
  },
  {
    id: 17,
    question: 'What is the largest land animal?',
    options: ['Elephant', 'Rhino', 'Giraffe', 'Hippo'],
    tags: ['animals', 'nature'],
    difficulty: 4,
  },
  {
    id: 18,
    question: 'What is the currency of Japan?',
    options: ['Yen', 'Yuan', 'Won', 'Ringgit'],
    tags: ['currency', 'countries'],
    difficulty: 3,
  },
  {
    id: 19,
    question: 'Which movie won the Oscar for Best Picture in 1994?',
    options: ['Forrest Gump', 'The Shawshank Redemption', 'The Lion King', 'Pulp Fiction'],
    tags: ['movies', 'Oscars'],
    difficulty: 4,
  },
  {
    id: 20,
    question: 'What is the largest country by land area?',
    options: ['Russia', 'Canada', 'United States', 'China'],
    tags: ['geography', 'countries'],
    difficulty: 5,
  },
])

const router = useRouter()

const availableTags = ref(getUniqueTags().map(tag => ({
  label: tag.charAt(0).toUpperCase() + tag.slice(1),
  value: tag.toLowerCase(),
})))

const tagQuery = ref([])
const filteredQuestions = computed(() => {
  if (tagQuery.value.length === 0)
    return allQuestions.value
  const searchTags = tagQuery.value.map(tag => tag.toLowerCase())
  return allQuestions.value.filter(question =>
    question.tags.some(tag => searchTags.includes(tag.toLowerCase())),
  )
})

function getUniqueTags() {
  const tags = new Set<string>()
  allQuestions.value.forEach((question) => {
    question.tags.forEach((tag) => {
      tags.add(tag)
    })
  })
  return Array.from(tags)
}

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
          clearable filterable multiple
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
