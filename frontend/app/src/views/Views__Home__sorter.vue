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
import { ref, watch } from "vue";
import { useLemmiStore } from "../store__lemmi";

const lemmiStore = useLemmiStore();

const sorting = ref("lemma ASC");

watch(sorting, async (newValue, oldValue) => {
  if (newValue !== oldValue) {
    const [order_by, order_value] = newValue.split(" ");
    lemmiStore.currentPageNumber = 1;
    lemmiStore.currentPage.metadata.offset = null;
    lemmiStore.currentPage.metadata.page_dir = "NEXT";
    lemmiStore.currentPage.metadata.order_by = order_by;
    lemmiStore.currentPage.metadata.order_value = order_value;
    await lemmiStore.fetchLemmi();
  }
});
</script>
