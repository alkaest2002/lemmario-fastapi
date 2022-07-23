<template>
  <div>
    <base-title>Cerca</base-title>
    <p class="mb-3">La ricerca produrrà un massimo di 20 risultati.</p>
    <Form
      v-slot="{ errors, isSubmitting, values: { lemma } }"
      :validation-schema="validationSchema"
      @submit="onSubmitForm"
      @invalid-submit="onInvalidSubmitForm"
    >
      <div class="field">
        <div class="control">
          <Field
            name="lemma"
            type="text"
            class="input is-medium"
            placeholder="inserisci almeno tre lettere"
            :class="{ 'is-danger': errors.lemma }"
          />
          <div class="has-text-danger">
            {{ errors.lemma }}
          </div>
        </div>
      </div>
      <div class="field">
        <div class="control">
          <Field
            v-slot="{ field }"
            name="isExactSearch"
            type="checkbox"
            :value="true"
          >
            <label>
              <input
                type="checkbox"
                name="isExactSearch"
                v-bind="field"
                :value="true"
              />
              <span class="hast-text-gray"> effettua ricerca esatta </span>
            </label>
          </Field>
          <div class="has-text-danger">
            {{ errors.isExactSearch }}
          </div>
        </div>
      </div>
      <div class="buttons">
        <base-loading-button
          v-model="isLoading"
          :type="'submit'"
          :button-css="'is-medium is-info'"
          :disabled="isSubmitting || !lemma"
          @click="searchType = 'SearchLemmi'"
        >
          Cerca
        </base-loading-button>
        <base-loading-button
          v-model="isLoading"
          :type="'submit'"
          :button-css="'is-medium is-warning'"
          :disabled="isSubmitting || !lemma"
          @click="searchType = 'SearchTreccani'"
        >
          Treccani
        </base-loading-button>
      </div>
      <div v-if="errors.apiError" class="has-text-danger mt-3 mb-0">
        {{ errors.apiError }}
      </div>
    </Form>
    <Suspense>
      <template #fallback>Attendere... </template>
       <search-lemmi :lemmi="lemmi" :result-is-ready="resultIsReady" />
    </Suspense>
  </div>
</template>

<script setup>
/* eslint-disable no-unused-vars */

import { ref, computed, onMounted } from "vue";
import { configure, Form, Field } from "vee-validate";
import { boolean, object, string } from "yup";

import { fetchWrapper } from "../utils__fetch";
import { searchUrl, searchUrlTreccani } from "../utils__urls";

import SearchLemmi from "./Components__Search_Lemmi.vue";

configure({
  validateOnBlur: false,
  validateOnChange: true,
  validateOnInput: false,
  validateOnModelUpdate: true,
});

const validationSchema = object().shape({
  lemma: string()
    .required("lemma richiesto")
    .min(3, "specifica almeno tre caratteri"),
  isExactSearch: boolean(),
});

const { get } = fetchWrapper;

const isLoading = ref(false);

const searchType = ref("SearchLemmi");

const resultIsReady = ref(false);

const lemmi = ref([]);

const computedUrl = computed(() => {
  console.log(searchType.value)
  if (searchType.value == "SearchTreccani")
    return searchUrlTreccani;
  return searchUrl
});

const onSubmitForm = async ({ lemma, isExactSearch }, { setErrors }) => {
  try {
    resultIsReady.value = false;
    const url = `${computedUrl.value}/${lemma}?${new URLSearchParams({
      isExactSearch: isExactSearch || false,
    })}`;
    lemmi.value = await get(url);
    resultIsReady.value = true;
  } catch (error) {
    setErrors({ apiError: error });
  } finally {
    isLoading.value = false;
  }
};

const onInvalidSubmitForm = () => {
  resultIsReady.value = false;
  isLoading.value = false;
};

onMounted(() => {
  const lemmaInput = document.getElementsByTagName("input")[0];
  lemmaInput.focus();
});
</script>
