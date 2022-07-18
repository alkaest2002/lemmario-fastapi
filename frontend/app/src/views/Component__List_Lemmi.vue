<template>
  <home-navigator />
  <div class="is-flex is-flex-direction-column is-justify-content-center my-4">
    <lemma-card
      v-for="(lemma, index) of lemmi"
      :key="index"
      :lemma="lemma"
      :selected-lemma-id="lemmiStore.currentSelectedLemmaId"
      @on-select-lemma="onSelectLemma"
    />
  </div>
  <home-navigator />
</template>

<script setup>
import { computed } from "vue";
import { useRouter } from "vue-router";
import { useLemmiStore } from "../store__lemmi";

import LemmaCard from "./Component__Lemma_Card.vue";
import HomeNavigator from "./Component__List_Navigator.vue";

const props = defineProps({
  getCache: {
    type: Boolean,
    default: false,
  },
});

const router = useRouter();

const lemmiStore = useLemmiStore();

const lemmi = computed(() => lemmiStore.currentPage.data.slice(0, -1));

const onSelectLemma = ({ lemmaId, isExpanded, isOverFlown }) => {
  lemmiStore.currentSelectedLemmaId = lemmaId;
  if ([isExpanded, !isExpanded && !isOverFlown].some(Boolean))
    router.push({
      name: "route-upsert-lemma",
      query: { scroll: window.pageYOffset },
    });
};

(async (getCache) => await lemmiStore.fetchLemmi(getCache))(props.getCache);
</script>
