<template>
  <router-view v-slot="{ Component }">
    <transition
      name="fade" 
      mode="out-in" 
      appear
    >
      <component 
        :is="Component"
        class="p-2"
      />
    </transition>
  </router-view>
</template>


<script setup>
</script>


<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
