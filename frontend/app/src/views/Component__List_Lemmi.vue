<template>
  <lemmi-navigator />
  <div class="is-flex is-flex-direction-column is-justify-content-center my-4">
    <div v-if="lemmi.length > 0">
      <lemma-card
        v-for="(lemma, index) of lemmi"
        :key="index"
        :lemma="lemma"
        :selected-lemma="lemmiStore.currentSelectedLemma"
        @on-select-lemma="onSelectLemma"
      />
    </div>
    <div v-else>
      <p class="has-text-gray mt-3">Nessun lemma trovato.</p>
    </div>
  </div>
  <lemmi-navigator v-if="lemmi.length > 0" />
</template>

<script setup>
import { computed } from "vue";
import { useLemma } from "../composables__lemma";

import LemmaCard from "./Component__Lemma_Card.vue";
import LemmiNavigator from "./Component__Lemmi_Navigator.vue";

const props = defineProps({
  getCache: {
    type: Boolean,
    default: false,
  },
});

const { lemmiStore, onSelectLemma } = useLemma();

const lemmi = computed(() => {
  if (lemmiStore.currentPage.data.length > lemmiStore.currentPage.metadata.page_size) 
    return lemmiStore.currentPage.data.slice(0, -1);
  return lemmiStore.currentPage.data;
});

(async (getCache) => await lemmiStore.fetchLemmi(getCache))(props.getCache);
</script>
