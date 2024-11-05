<!--
  @author: adibarra (Alec Ibarra)
  @description: This component is used to display the default layout of the application.
-->

<template>
  <div flex grow flex-col bg--c-primary text--c-text min-h-svh>
    <PullToRefresh />
    <Header />
    <RouterView />
    <Footer />
  </div>
</template>
