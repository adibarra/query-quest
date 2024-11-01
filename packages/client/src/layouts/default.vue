<!--
  @author: adibarra (Alec Ibarra)
  @description: This component is used to display the default layout of the application.
-->

<template>
  <PullToRefresh />
  <Header>
    <TitleLogo hidden text-3xl sm:block />
  </Header>
  <RouterView />
  <Footer />
</template>
