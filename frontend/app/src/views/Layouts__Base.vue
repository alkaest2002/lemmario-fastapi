<template>
  <div id="main" class="container is-max-desktop p-6">
    <div class="is-flex is-flex-direction-column is-justify-content-center">
      <slot />
    </div>
  </div>
</template>

<script>
export default {
  name: "BaseLayout",
};
</script>

<style lang="scss" scoped>
#main {
  height: 100vh;

  > div {
    height: 100%;
    width: 100%;
  }
}
</style>
