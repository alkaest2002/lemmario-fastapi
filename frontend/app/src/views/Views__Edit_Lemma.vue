<template>
  {{ selectedLemma }}
</template>

<script setup>
import { reactive } from  "vue";
import { useLemmiStore  } from "../store__lemmi";

const lemmiStore = useLemmiStore();

const selectedLemma = reactive(lemmiStore.currentSelectedLemma);

</script>