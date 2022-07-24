<template>
  <div v-if="lemmi.length > 0" class="mt-5">
    <div class="is-flex is-flex-direction-column is-justify-content-center">
      <lemma-card
        v-for="lemma of lemmi"
        :key="lemma"
        :lemma="lemma"
        :selected-lemma="lemmiStore.currentSelectedLemma"
        @on-select-lemma="onSelectLemma"
      />
    </div>
  </div>
  <div v-if="lemmi.length == 0 && resultIsReady" class="mt-5">
    Nessun risultato.
  </div>
</template>

<script setup>
/* eslint-disable no-unused-vars */
import { useLemma } from "../composables__lemma";
import LemmaCard from "./Component__Lemma_Card.vue";

const props = defineProps({
  lemmi: {
    type: Array,
    default: () => {
      [];
    },
  },

  resultIsReady: {
    type: Boolean,
    default: false,
  },
});

const { lemmiStore, onSelectLemma } = useLemma();
</script>
