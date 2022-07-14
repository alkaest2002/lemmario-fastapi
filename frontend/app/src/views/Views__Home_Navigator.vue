<template>
 <div class="is-flex is-justify-content-space-between">
    <lemmi-sorter />
    <div class="buttons are-medium">
      <lemmi-paginator />
      <router-link class="button is-warning" :to="{ name: 'route-search-lemma'}">
          Cerca
      </router-link>
    </div>
  </div>
</template>

<script setup>
  import LemmiPaginator from "./Views__Home_Paginator.vue";
  import LemmiSorter from "./Views__Home__Sorter.vue";
</script>