<template>
  <div class="select is-medium">
    <select v-model="sorting">
      <option value="lemma ASC">Lemma ASC</option>
      <option value="lemma DESC">Lemma DESC</option>
      <option value="updated ASC">Updated ASC</option>
      <option value="updated DESC">Updated DESC</option>
    </select>
  </div>
</template>

<script setup>
/* eslint-disable no-unused-vars */
import { computed, watch } from "vue";
import { useLemmiStore } from "../store__lemmi";

const lemmiStore = useLemmiStore();

const sorting = computed({
  get: () => {
    if (lemmiStore.currentPage.metadata.order_by)
      return `${lemmiStore.currentPage.metadata.order_by} ${lemmiStore.currentPage.metadata.order_value}`;
    return "lemma ASC";
  },
  set: async (newSorting) => {
    const currentSorting = 
      `${lemmiStore.currentPage.metadata.order_by} ${lemmiStore.currentPage.metadata.order_value}`;
    if (newSorting !== currentSorting) {
      const [order_by, order_value] = newSorting.split(" ");
      lemmiStore.currentPageNumber = 1;
      lemmiStore.currentPage.metadata.offset = null;
      lemmiStore.currentPage.metadata.page_dir = "NEXT";
      lemmiStore.currentPage.metadata.order_by = order_by;
      lemmiStore.currentPage.metadata.order_value = order_value;
      await lemmiStore.fetchLemmi();
    }
  }
});
</script>
