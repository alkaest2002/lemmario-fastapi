<template>
  <div>
    <h2 class="is-size-2 has-text-weight-bold mb-4">Home</h2>
    <div class="is-flex is-flex-direction-column is-justify-content-center">
      <div 
        v-for="lemma of lemmi" :key="lemma.rowid"
        class="card my-2"
      >
        <div class="card-content">
          <p class="is-size-5 has-text-weight-bold">
            {{ lemma.lemma }}
          </p>
          <p>
            {{ lemma.definition }}
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted } from "vue";
import { useLemmiStore } from "../store__lemmi";

const lemmiStore = useLemmiStore();

const lemmi = computed(() => lemmiStore.data);

onMounted(async () => {
  try {
    await lemmiStore.fetchLemmi()
  } catch(error) {
    console.log(error)
  }
});
</script>
