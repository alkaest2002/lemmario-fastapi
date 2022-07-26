<template>
  <div>
    <base-title>Cerca</base-title>
    <p class="mb-3">La ricerca produrrà un massimo di 20 risultati.</p>
    <search-form
      :result-is-ready="resultIsReady"
      @on-search-lemma="onSearchLemma"
    />
    <Suspense>
      <template #fallback>Attendere... </template>
      <search-list :lemmi="lemmi" :result-is-ready="resultIsReady" />
    </Suspense>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { fetchWrapper } from "../utils__fetch";
import { searchUrl, searchUrlTreccani, searchUrlOlivetti } from "../utils__urls";
import SearchForm from "./Forms__Search.vue";
import SearchList from "./Components__Search_List.vue";

const { get } = fetchWrapper;

const resultIsReady = ref(false);

const lemmi = ref([]);

const computeUrl = (searchType) => {
  const urls = {
    "lemmi": searchUrl,
    "treccani": searchUrlTreccani,
    "olivetti": searchUrlOlivetti
  };
  return Object.keys(urls).includes(searchType)
    ? urls[searchType]
    : urls["lemmi"];
};

const onSearchLemma = async ({
  formData: { lemma, exact },
  searchType,
  setErrors,
}) => {
  try {
    resultIsReady.value = false;
    const computedUrl = computeUrl(searchType)
    const url = `${computedUrl}/${lemma}?${new URLSearchParams({ exact })}`;
    lemmi.value = await get(url);
  } catch (error) {
    setErrors({ apiError: error });
  } finally {
    resultIsReady.value = true;
  }
};
</script>
