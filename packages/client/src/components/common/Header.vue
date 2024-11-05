<!--
  @author: adibarra (Alec Ibarra)
  @description: This component is used to display the header of the application.
-->

<template>
  <header h-48px w-full flex b-b-1 b-b--c-tertiary bg--c-primary>
    <div flex grow items-center py-1>
      <div hidden h-full w-55 items-center justify-center md:flex>
        <Logo />
      </div>
      <div grow />
      <nav my-auto mr-5 flex gap-5 sm:text-xl>
        <RouterLink
          to="/"
          title="Home"
          qq-icon-btn
        >
          <div i-carbon:home />
        </RouterLink>
        <ThemeSwitch />
      </nav>
    </div>
  </header>
</template>
