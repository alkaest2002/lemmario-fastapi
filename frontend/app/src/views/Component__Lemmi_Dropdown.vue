<template>
  <div class="dropdown is-right" :class="{'is-active': dropDownIsActive}">
    <div class="dropdown-trigger">
      <button class="button is-medium is-primary" @click="dropDownIsActive = !dropDownIsActive">
        <img src="/src/assets/svg/cog.svg">
      </button>
    </div>
    <div id="filter-and-sort" class="dropdown-menu" role="menu">
      <div class="dropdown-content">
        <div class="dropdown-item is-flex is-flex-wrap-wrap is-justify-content-space-between">
          <div 
            v-for="letter in letters" 
            :key="letter"
            class="filter-value is-clickable mr-3 is-flex is-justify-content-center is-align-items-center"
            :class="{ 'is-active': letter == filteredLetter }"
            @click="filteredLetter = letter"
          >
            <div class="p-1">
              {{ letter }}
            </div>
          </div>
          <div 
            class="filter-value is-clickable mr-3 is-flex is-justify-content-center is-align-items-center is-flex-grow-1" 
            :class="{ 'is-active': !filteredLetter }"
            @click="filteredLetter = null"
          >
            <div class="p-1">
              Tutto
            </div>
          </div>
        </div>
        <hr class="dropdown-divider">
         <div class="dropdown-item">
            <div
              v-for="orderBy of possibleOrderBy"
              :key="orderBy"
              class="order-value is-clickable"
              :class="{ 'is-active': orderBy == selectedOrderBy }"
              @click="selectedOrderBy = orderBy"
            >
              <div class="p-1">
                {{ orderBy.charAt(0).toUpperCase() + orderBy.slice(1) }}
              </div>
            </div>
         </div>
        <hr class="dropdown-divider">
        <div class="dropdown-item">
          <div class="buttons">
            <base-loading-button
              v-model="isLoading"
              class="button is-primary is-fullwidth"
              @click="onApplyFilterAndSorting"
            >
              applica
            </base-loading-button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>


<script setup>
import { ref, computed } from "vue";
import { useLemmiStore } from "../store__lemmi";

const letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ".split("");

const possibleOrderBy = ["lemma ASC", "lemma DESC", "updated ASC", "updated DESC"]

const lemmiStore = useLemmiStore();

const isLoading = ref(false)

const dropDownIsActive = ref(false);

const filterByLetter = ref(false);

const filteredLetter = computed({
  get: () => {
    return lemmiStore.currentPage.metadata.filter_value;
  },
  set: (newLetter) => {
    filterByLetter.value = true
    if (lemmiStore.currentPage.metadata.filter_value !== newLetter) {
      lemmiStore.currentPageNumber = 1;
      lemmiStore.currentPage.metadata.offset = null;
      lemmiStore.currentPage.metadata.page_dir = "NEXT";
      lemmiStore.currentPage.metadata.filter_by = newLetter ? "letter" : null;
      lemmiStore.currentPage.metadata.filter_value = newLetter;
    }
  },
});

const selectedOrderBy = computed({
  get: () => {
    return `${lemmiStore.currentPage.metadata.order_by} ${lemmiStore.currentPage.metadata.order_value}`
  },
  set: (newOrderBy) => {
    const [ order_by, order_value ] = newOrderBy.split(" ");
    lemmiStore.currentPage.metadata.order_by = order_by;
    lemmiStore.currentPage.metadata.order_value = order_value;
  }
});

const onApplyFilterAndSorting = async() => {
 await lemmiStore.fetchLemmi();
 isLoading.value = false;
 dropDownIsActive.value = false;
}
</script>

<style lang="scss" scoped>
  img {
    height: 24px;
  }
  .filter-value {
    width: 28px;
    border: 1px solid transparent;
    &.is-active {
      background-color: #ddd;
      border-radius: 3px;
    }
  }

   .order-value {
    border: 1px solid transparent;
    &.is-active {
      background-color: #ddd;
      border-radius: 3px;
    }
  }
</style>