<template>
  <div class="is-flex is-justify-content-space-between">
    <div>
      <lemmi-filter class="mr-2" />
      <lemmi-sorter />
    </div>
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
import LemmiPaginator from "./Component__Lemmi_Paginator.vue";
import LemmiFilter from "./Component__Lemmi_Filter.vue";
import LemmiSorter from "./Component__Lemmi_Sorter.vue";
</script>
