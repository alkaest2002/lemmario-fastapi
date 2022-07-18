<template>
  <div class="is-flex is-justify-content-space-between">
    <lemmi-sorter />
    <div class="buttons are-medium ml-3">
      <lemmi-paginator />
      <router-link
        class="button is-warning"
        :to="{ name: 'route-search-lemma' }"
      >
        Cerca
      </router-link>
    </div>
  </div>
</template>

<script setup>
import LemmiPaginator from "./Component__List_Paginator.vue";
import LemmiSorter from "./Component__List_Sorter.vue";
</script>
