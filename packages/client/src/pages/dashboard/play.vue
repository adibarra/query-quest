<!--
  @author: adibarra (Alec Ibarra)
  @description: This component is used to display the play page of the application.
-->

<script setup lang="ts">
useHead({
  title: `Play • QueryQuest`,
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

const router = useRouter()
const route = useRoute()

const currentQuestionId = ref(Number(route.query.id) || 1)
const currentQuestion = computed(() => allQuestions.value.find(q => q.id === currentQuestionId.value) || allQuestions.value[0])

const isQuestionVisible = ref(true)
const areOptionsVisible = ref(false)
const isResultVisible = ref(false)
const userAnswer = ref<string | null>(null)
const isCorrect = computed(() => userAnswer.value === currentQuestion.value.options[0])

const scrambledOptions = computed(() => {
  const options = [...currentQuestion.value.options]
  for (let i = options.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1))
    ;[options[i], options[j]] = [options[j], options[i]]
  }
  return options
})

function showOptions() {
  isQuestionVisible.value = true
  areOptionsVisible.value = false
  userAnswer.value = null
  isResultVisible.value = false

  setTimeout(() => {
    areOptionsVisible.value = true
  }, 2000)
}

function selectAnswer(answer: string) {
  userAnswer.value = answer
  areOptionsVisible.value = false
  isResultVisible.value = true
}

function loadRandomQuestion() {
  const randomIndex = Math.floor(Math.random() * allQuestions.value.length)
  currentQuestionId.value = allQuestions.value[randomIndex].id
  showOptions()
}

function goToDashboard() {
  router.push('/dashboard')
}

watch(() => route.query.id, () => {
  currentQuestionId.value = Number(route.query.id) || 1
  showOptions()
})

showOptions()
</script>

<template>
  <main h-full w-full flex flex-col items-center justify-center>
    <div v-if="isQuestionVisible" mb-4 text-2xl font-semibold>
      {{ currentQuestion.question }}
    </div>

    <div v-show="areOptionsVisible" class="flex flex-col gap-2">
      <NButton
        v-for="option in scrambledOptions"
        :key="option"
        type="default"
        size="large"
        class="option-button"
        @click="selectAnswer(option)"
      >
        {{ option }}
      </NButton>
    </div>

    <div v-show="isResultVisible" class="result mt-4 text-center">
      <p :class="{ 'text-green-500': isCorrect, 'text-red-500': !isCorrect }" text-2xl font-bold>
        {{ isCorrect ? 'Correct! 🎉' : 'Oops, try again! ❌' }}
      </p>

      <div mt-2 text-xl text-blue-500>
        +10 XP
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
.result {
  transform: scale(0.8);
  transition:
    transform 0.5s ease-in-out,
    opacity 0.5s ease-in-out;
}
.result[style*='display: block;'] {
  transform: scale(1);
}

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
