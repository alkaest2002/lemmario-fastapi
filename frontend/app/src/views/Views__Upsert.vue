<template>
  <div>
    <base-title>
      {{ selectedLemma.rowid ? "Modifica" : "Inserisci" }}
    </base-title>
    <upsert-form
      :initial-values="cleanedSelectedLemma"
      :result-is-ready="resultIsReady"
      @on-upsert-lemma="onUpsertLemma"
      @on-delete-lemma="onDeleteLemma"
    >
      <template #upsertButtonLabel>
        {{ selectedLemma.rowid ? "Modifica" : "Inserisci" }}
      </template>
    </upsert-form>
  </div>
</template>

<script setup>
import { ref, computed } from "vue";
import { useRoute } from "vue-router";
import { useLemmiStore } from "../store__lemmi";
import { fetchWrapper } from "../utils__fetch";
import { insertUrl, editUrl, deleteUrl } from "../utils__urls";
import { router } from "../router__main";
import UpsertForm from "./Forms__Upsert.vue";

const lemmiStore = useLemmiStore();

const { post, put, del } = fetchWrapper;

const route = useRoute();

const resultIsReady = ref(false);

const selectedLemma = lemmiStore.currentSelectedLemma;

const cleanedSelectedLemma = computed(() => {
  let lemma = { ...selectedLemma };
  Object.keys(lemma).forEach((key) => {
    const regex = /<b>|<\/b>/gi;
    if (typeof lemma[key] == "string")
      lemma[key] = lemma[key].replace(regex, "");
  });
  return lemma;
});

const onUpsertLemma = async ({ formData, setErrors }) => {
  try {
    resultIsReady.value = false;
    const upsertUrl = selectedLemma.rowid
      ? `${editUrl}/${selectedLemma.rowid}`
      : insertUrl;
    const restOp = selectedLemma.rowid ? put : post;
    const lemmaToUpsert = await restOp(upsertUrl, { payload: formData });
    lemmiStore.updateLemma(lemmaToUpsert);
    router.push({
      name: "route-list",
      query: { scroll: route.query.scroll },
    });
  } catch (error) {
    setErrors({ apiError: error });
  } finally {
    resultIsReady.value = true;
  }
};

const onDeleteLemma = async ({ setErrors }) => {
  try {
    resultIsReady.value = false;
    await del(`${deleteUrl}/${selectedLemma.rowid}`);
    router.push({
      name: "route-list",
      query: { scroll: route.query.scroll },
    });
  } catch (error) {
    setErrors({ apiError: error });
  } finally {
    resultIsReady.value = true;
  }
};
</script>
