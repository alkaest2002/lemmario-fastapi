<template>
  <div>
    <h2 class="is-size-2 has-text-weight-bold mb-4">Home</h2>
    <div class="is-flex is-justify-content-space-between mb-3">
      <lemmi-sorter />
      <lemmi-paginator />
    </div>
    <div class="is-flex is-flex-direction-column is-justify-content-center">
      <lemma-card
        v-for="lemma of lemmi"
        :key="lemma.rowid"
        :lemma="lemma"
        :selected-lemma-id="lemmiStore.currentSelectedLemmaId"
        @on-select-lemma="onSelectLemma"
      />
    </div>
    <div class="is-flex is-justify-content-space-between mt-3">
      <lemmi-sorter />
      <lemmi-paginator />
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted } from "vue";
import { useRouter } from "vue-router";
import { useLemmiStore } from "../store__lemmi";
import LemmaCard from "./Views__Home_Lemma.vue";
import LemmiPaginator from "./Views__Home_paginator.vue";
import LemmiSorter from "./Views__Home__sorter.vue";

const router = useRouter();

const lemmiStore = useLemmiStore();

const lemmi = computed(() => lemmiStore.currentPage.data.slice(0, -1));

const onSelectLemma = ({ lemmaId, className, isOverFlown }) => {
  lemmiStore.currentSelectedLemmaId = lemmaId;
  if (className.indexOf("is-expanded") > -1) {
    router.push({ name: "route-edit-lemma"});
  } else {
    if (!isOverFlown)
      router.push({ name: "route-edit-lemma"});
  }
}

onMounted(async () => {
  try {
    await lemmiStore.fetchLemmi();
  } catch (error) {
    console.log(error);
  }
});
</script>
