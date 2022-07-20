<template>
  <lemmi-navigator />
  <div class="is-flex is-flex-direction-column is-justify-content-center my-4">
    <lemma-card
      v-for="(lemma, index) of lemmi"
      :key="index"
      :lemma="lemma"
      :selected-lemma="lemmiStore.currentSelectedLemma"
      @on-select-lemma="onSelectLemma"
    />
  </div>
  <lemmi-navigator />
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

const lemmi = computed(() => lemmiStore.currentPage.data.slice(0, -1));

(async (getCache) => await lemmiStore.fetchLemmi(getCache))(props.getCache);
</script>
