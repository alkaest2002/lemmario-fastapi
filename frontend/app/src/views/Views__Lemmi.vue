<template>
  <div>
    <base-title>Lemmario.com</base-title>
    <Suspense>
      <template #fallback>Attendere... </template>
      <lemmi-list :get-cache="'scroll' in route.query" />
    </Suspense>
  </div>
</template>

<script setup>
import { useRoute } from "vue-router";
import LemmiList from "./Component__Lemmi.vue";

const route = useRoute();

if (route.query.scroll) {
  setTimeout(() => window.scrollTo(0, route.query.scroll), 0);
}
</script>
