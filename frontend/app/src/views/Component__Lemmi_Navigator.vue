<template>
  <div class="is-flex is-justify-content-space-between">
    <div class="buttons are-medium">
      <lemmi-paginator />
      <lemmi-search />
    </div>
    <lemmi-dropdown />
  </div>
</template>

<script setup>
import LemmiPaginator from "./Component__Lemmi_Paginator.vue";
import LemmiDropdown from "./Component__Lemmi_Dropdown.vue";
import LemmiSearch from "./Component__Lemmi_Search.vue"
</script>
