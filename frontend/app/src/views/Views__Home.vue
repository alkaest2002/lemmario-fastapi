<template>
  <div>
    <h2 class="is-size-2 has-text-weight-bold mb-4">Home</h2>
    <div class="is-flex is-flex-direction-column is-justify-content-center">
      <base-lemma 
        v-for="lemma of lemmi" 
        :key="lemma.rowid" 
        v-model="clickedLemma"
        :lemma="lemma"
      />
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted } from "vue";
import { useLemmiStore } from "../store__lemmi";
import baseLemma from "./Base__Lemma.vue";

const lemmiStore = useLemmiStore();

const lemmi = computed(() => lemmiStore.currentPage.data);

const clickedLemma = computed({
  get() { return lemmiStore.currentExpandendItemId },
  set(value) { lemmiStore.currentExpandendItemId = value }
}); 

onMounted(async () => {
  try {
    await lemmiStore.fetchLemmi()
  } catch(error) {
    console.log(error)
  }
});
</script>
