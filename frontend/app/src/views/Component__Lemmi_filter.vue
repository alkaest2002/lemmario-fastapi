<template>
  <div class="select is-medium">
    <select v-model="filtering">
      <option :value="'letter tutto'">Tutto</option>
      <option v-for="letter in letters" :key="letter" :value="`letter ${letter}`">
        {{ letter }}
      </option>
    </select>
  </div>
</template>

<script setup>
import { computed } from "vue";
import { useLemmiStore } from "../store__lemmi";

const letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ".split("");

const lemmiStore = useLemmiStore();

const filtering = computed({
  get: () => {
    if (lemmiStore.currentPage.metadata.filter_by)
      return `${lemmiStore.currentPage.metadata.filter_by} ${lemmiStore.currentPage.metadata.filter_value}`;
    return "letter tutto";
  },
  set: async (newFiltering) => {
    const currentFiltering = `${lemmiStore.currentPage.metadata.filter_by} ${lemmiStore.currentPage.metadata.filter_value}`;
    if (newFiltering !== currentFiltering) {
      const [filter_by, filter_value] = newFiltering.split(" ");
      lemmiStore.currentPageNumber = 1;
      lemmiStore.currentPage.metadata.offset = null;
      lemmiStore.currentPage.metadata.page_dir = "NEXT";
      lemmiStore.currentPage.metadata.filter_by = filter_value == "tutto" ? null : filter_by;
      lemmiStore.currentPage.metadata.filter_value = filter_value == "tutto" ? null : filter_value;
      await lemmiStore.fetchLemmi();
    }
  },
});
</script>
