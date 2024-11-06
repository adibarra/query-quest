<!--
  @author: adibarra (Alec Ibarra)
  @description: This component is used to display the home page of the application.
-->

<script setup lang="ts">
useHead({
  title: `Dashboard • QueryQuest`,
})

const router = useRouter()

// Mock data to simulate DB content (replace with actual API calls as needed)
const allQuestions = ref([
  {
    id: 1,
    question: 'What is the capital of France?',
    options: ['Paris', 'London', 'Berlin', 'Madrid'],
    tags: ['geography', 'countries'],
    difficulty: 2, // Difficulty rating 1 to 5
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
    options: ['0', '1', '2', '3'],
    tags: ['math', 'numbers'],
    difficulty: 1,
  },
  {
    id: 4,
    question: 'Which planet is known as the Red Planet?',
    options: ['Earth', 'Mars', 'Jupiter', 'Venus'],
    tags: ['science', 'astronomy'],
    difficulty: 2,
  },
  {
    id: 5,
    question: 'What is the largest ocean on Earth?',
    options: ['Atlantic Ocean', 'Indian Ocean', 'Arctic Ocean', 'Pacific Ocean'],
    tags: ['geography', 'oceans'],
    difficulty: 4,
  },
  {
    id: 6,
    question: 'Who painted the Mona Lisa?',
    options: ['Vincent van Gogh', 'Leonardo da Vinci', 'Pablo Picasso', 'Claude Monet'],
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
    options: ['China', 'South Korea', 'Japan', 'Vietnam'],
    tags: ['geography', 'countries'],
    difficulty: 2,
  },
  {
    id: 14,
    question: 'What is the main ingredient in guacamole?',
    options: ['Tomato', 'Avocado', 'Onion', 'Garlic'],
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
    options: ['Abraham Lincoln', 'Thomas Jefferson', 'George Washington', 'John Adams'],
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
    options: ['Yuan', 'Won', 'Yen', 'Ringgit'],
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
    options: ['Canada', 'Russia', 'United States', 'China'],
    tags: ['geography', 'countries'],
    difficulty: 5,
  },
])

// Function to extract unique tags from all questions
function getUniqueTags() {
  const tags = new Set<string>()
  allQuestions.value.forEach((question) => {
    question.tags.forEach((tag) => {
      tags.add(tag)
    })
  })
  return Array.from(tags)
}

// Replace the availableTags array with dynamic tags from questions
const availableTags = ref(getUniqueTags().map(tag => ({
  label: tag.charAt(0).toUpperCase() + tag.slice(1), // Capitalize first letter
  value: tag.toLowerCase(),
})))

// States for UI controls
const tagQuery = ref([])
const filteredQuestions = computed(() => {
  if (tagQuery.value.length === 0)
    return allQuestions.value
  const searchTags = tagQuery.value.map(tag => tag.toLowerCase())
  return allQuestions.value.filter(question =>
    question.tags.some(tag => searchTags.includes(tag.toLowerCase())),
  )
})

// Function to navigate to the play page with the question ID
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
      <!-- Search by Tag -->
      <div class="max-w-md w-full flex flex-col gap-2">
        <label for="tag-search" class="text--c-inverse font-medium">Search by Tag:</label>
        <NSelect
          placeholder="Select or type tags"
          clearable
          multiple
          filterable
          :options="availableTags"
          @update:value="(value) => tagQuery = value"
        />
      </div>

      <NButton
        type="primary"
        size="large"
        class="mt-auto max-w-100 bg--c-secondary text--c-inverse"
        @click="loadRandomQuestion"
      >
        Answer Random Trivia Question
      </NButton>
    </div>

    <!-- Filtered Questions by Tag -->
    <div v-if="filteredQuestions.length" class="filtered-questions mt-4">
      <div class="mt-2 space-y-4">
        <NCard
          v-for="question in filteredQuestions"
          :key="question.id"
          :title="question.question"
          class="rounded-md bg--c-secondary p-4 shadow-md"
        >
          <div flex flex-row justify-between>
            <div flex flex-col gap-2>
              <div class="flex">
                <span>Difficulty:</span>
                <NRate :default-value="question.difficulty" readonly />
              </div>

              <div class="flex gap-2">
                <span>Tags:</span>
                <div class="flex gap-1">
                  <NTag v-for="tag in question.tags" :key="tag" type="success" size="small">
                    {{ tag }}
                  </NTag>
                </div>
              </div>
            </div>

            <!-- Play Button aligned to the right -->
            <NButton
              type="primary"
              size="small"
              class="bg--c-tertiary text--c-inverse"
              @click="goToPlayPage(question.id)"
            >
              Play
            </NButton>
          </div>
        </NCard>
      </div>
    </div>

    <!-- No results found -->
    <div v-else-if="tagQuery" class="no-results mt-4">
      <p class="text--c-inverse italic">
        No questions found for tag "{{ tagQuery }}"
      </p>
    </div>
  </main>
</template>

<route lang="yaml">
  meta:
    layout: dashboard
</route>
