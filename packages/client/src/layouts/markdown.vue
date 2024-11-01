<template>
  <PullToRefresh />
  <Header>
    <TitleLogo hidden text-3xl sm:block />
  </Header>
  <div class="dots">
    <div min-h-full w-full px-6 py-4>
      <div mx-auto max-w-full w-fit bg--c-secondary px-4 py-4 sm:px-16 class="receipt">
        <RouterView />
        <a
          title="Go Back"
          tg-icon-btn mx-auto my-20 w-fit flex text-lg
          @click="$router.back()"
          @keydown.enter="$router.back()"
        >
          <div i-carbon:caret-left text-2xl />
          Go Back
        </a>
      </div>
    </div>
    <Footer />
  </div>
</template>

<style>
.prose pre:not(.shiki) {
  padding: 0;
}

.prose .shiki {
  font-family: 'DM Mono', monospace;
  font-size: 1.2em;
  line-height: 1.4;
  background: var(--c-bg);
}

.prose img {
  width: 100%;
}

.shiki,
.shiki span {
  color: var(--shiki-light);
}

html.dark .shiki,
html.dark .shiki span {
  color: var(--shiki-dark);
}
</style>

<style scoped>
.dots {
  background-image: radial-gradient(var(--c-tertiary) 1px, transparent 0);
  background-size: 2rem 2rem;
}

/* https://css-generators.com/custom-borders/ */
.receipt {
  --mask: conic-gradient(from 125deg at top, #0000, #000 1deg 109deg, #0000 110deg) top/28.56px 51% repeat-x,
    conic-gradient(from -55deg at bottom, #0000, #000 1deg 109deg, #0000 110deg) calc(50% + 14.28px) 100%/28.56px 51%
      repeat-x;
  -webkit-mask: var(--mask);
  mask: var(--mask);
}
</style>
