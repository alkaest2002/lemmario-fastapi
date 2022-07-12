<template>
  <nav class="pagination is-medium is-rounded" role="navigation" aria-label="pagination">
    <a 
      class="pagination-previous"
      :class="{ 'is-disabled' : lemmiStore.currentPageNumber == 1 }"
      @click="onClickNav('PREV')"
    >Prec</a>
    <a 
      class="pagination-next"
      @click="onClickNav('NEXT')"
    >Succ</a>
  </nav>
</template>

<script setup>
import { useLemmiStore } from "../store__lemmi";

const lemmiStore = useLemmiStore();

const onClickNav = async (pageDirection) => {
  lemmiStore.updateCurrentPageNumber(pageDirection);
  lemmiStore.currentPage.metadata.page_dir = pageDirection;
  lemmiStore.currentPage.metadata.offset = pageDirection == "NEXT"
    ? lemmiStore.currentPage.data.slice(-1)[0][lemmiStore.currentPage.metadata.order_by]
    : lemmiStore.currentPage.data[0][lemmiStore.currentPage.metadata.order_by];
  await lemmiStore.fetchLemmi();
};

</script>