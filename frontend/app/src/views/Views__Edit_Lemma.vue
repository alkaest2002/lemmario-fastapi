<template>
  <div>
    <h2 class="is-size-2 has-text-weight-bold mb-4">Home</h2>
    {{ selectedLemma }}
  </div>
</template>

<script setup>
import { reactive } from "vue";
import { useLemmiStore } from "../store__lemmi";

const lemmiStore = useLemmiStore();

const selectedLemma = reactive(lemmiStore.currentSelectedLemma);
</script>
