<template>
  <button
    class="button is-info"
    :disabled="lemmiStore.currentPageNumber == 1"
    @click.prevent="onClickNav('PREV')"
  >
    &larr;
  </button>
  <button
    class="button is-info"
    :disabled="
      lemmiStore.currentPage.data.length <
      lemmiStore.currentPage.metadata.page_size + 1
    "
    @click.prevent="onClickNav('NEXT')"
  >
    &rarr;
  </button>
</template>

<script setup>
import { useLemmiStore } from "../store__lemmi";

const lemmiStore = useLemmiStore();

const onClickNav = async (pageDirection) => {
  lemmiStore.updateCurrentPageNumber(pageDirection);
  lemmiStore.currentPage.metadata.page_dir = pageDirection;
  lemmiStore.currentPage.metadata.offset =
    pageDirection == "NEXT"
      ? lemmiStore.currentPage.data.slice(-1)[0][
          lemmiStore.currentPage.metadata.order_by
        ]
      : lemmiStore.currentPage.data[0][
          lemmiStore.currentPage.metadata.order_by
        ];
  await lemmiStore.fetchLemmi();
};
</script>
