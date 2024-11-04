<!--
  @author: adibarra (Alec Ibarra)
  @description: This component is used to display the header of the application.
-->

<template>
  <header relative sticky top-0 z-999 flex b-b-1 b-b--c-tertiary bg--c-primary px-3 py-2 sm:py-3>
    <div absolute left-0 right-0 my-auto>
      <slot />
    </div>
    <RouterLink
      to="/"
      title="Logo"
      op-100 qq-icon-btn
    >
      <div i-carbon:unknown text-2xl sm:text-4xl />
    </RouterLink>
    <div grow />
    <nav my-auto flex gap-x5 sm:text-xl>
      <RouterLink
        to="/"
        title="Home"
        qq-icon-btn
      >
        <div i-carbon:home />
      </RouterLink>
      <a
        href="https://github.com/adibarra/query-quest"
        target="_blank"
        rel="noopener"
        title="GitHub Repository"
        qq-icon-btn
      >
        <div i-carbon:logo-github />
      </a>
      <button
        title="Toggle Theme"
        qq-icon-btn
        @click="toggleTheme()"
        @keydown.enter="toggleTheme()"
      >
        <div i="carbon-sun dark:carbon-moon" />
      </button>
    </nav>
  </header>
</template>
