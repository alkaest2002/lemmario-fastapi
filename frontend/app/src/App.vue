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

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
  background-color: ghostwhite;
}
</style>
