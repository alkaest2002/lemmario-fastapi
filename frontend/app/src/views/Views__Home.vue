<template>
  <div>
    <h2 class="is-size-2 has-text-weight-bold mb-6">Lemmario.com</h2>
    <home-navigator />
    <div class="is-flex is-flex-direction-column is-justify-content-center my-4">
      <lemma-card
        v-for="lemma of lemmi"
        :key="lemma.rowid"
        :lemma="lemma"
        :selected-lemma-id="lemmiStore.currentSelectedLemmaId"
        @on-select-lemma="onSelectLemma"
      />
    </div>
    <home-navigator />
  </div>
</template>

<script setup>
import { computed, onMounted } from "vue";
import { useRouter, useRoute } from "vue-router";
import { useLemmiStore } from "../store__lemmi";
import LemmaCard from "./Views__Home_Lemma.vue";
import HomeNavigator from "./Views__Home_Navigator.vue";

const router = useRouter();

const route = useRoute();

const lemmiStore = useLemmiStore();

const lemmi = computed(() => lemmiStore.currentPage.data.slice(0, -1));

const onSelectLemma = ({ lemmaId, isExpanded, isOverFlown }) => {
  lemmiStore.currentSelectedLemmaId = lemmaId;
  if ([isExpanded, !isExpanded && !isOverFlown].some(Boolean))
    router.push({ name: "route-edit-lemma", params: { position: window.pageYOffset }});
};

onMounted(async () => {
  try {
    await lemmiStore.fetchLemmi();
    if (route.params.position)
      window.scrollTo(0, route.params.position);
  } catch (error) {
    console.log(error);
  }
});
</script>
