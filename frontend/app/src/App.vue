<template>
  <router-view v-slot="{ Component }">
    <transition name="fade" mode="out-in" appear>
      <base-layout>
        <component :is="Component" />
      </base-layout>
    </transition>
  </router-view>
</template>

<script setup>
import { watch } from "vue";
import { useAuthStore } from "./store__auth";
import { router } from "./router__main";

const authStore = useAuthStore();

watch(
  () => authStore.accessToken,
  (newValue) => {
    if (newValue == null) router.push({ name: "route-login" });
  }
);
</script>

<style lang="scss">
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.5s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
  transition: opacity 0, 0.5s;
}
</style>
