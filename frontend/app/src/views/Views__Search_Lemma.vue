<template>
  <div>
    <base-title :title="'Cerca'" />
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
      <div class="control">
        <base-loading-button
          v-model="isLoading"
          :type="'submit'"
          :button-css="'is-medium is-info'"
          :disabled="isSubmitting || !lemma"
        >
          Cerca
        </base-loading-button>
      </div>
      <div v-if="errors.apiError" class="has-text-danger mt-3 mb-0">
        {{ errors.apiError }}
      </div>
    </Form>
    <div v-if="lemmi.length > 0" class="mt-5">
      <div class="is-flex is-flex-direction-column is-justify-content-center">
        <lemma-card
          v-for="(lemma, index) of lemmi"
          :key="index"
          :lemma="lemma"
          :selected-lemma="lemmiStore.currentSelectedLemma"
          @on-select-lemma="onSelectLemma"
        />
      </div>
    </div>
    <div v-if="lemmi.length == 0 && resultIsReady" class="mt-5">
      Nessun risultato.
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { configure, Form, Field } from "vee-validate";
import { boolean, object, string } from "yup";

import { fetchWrapper } from "../utils__fetch";
import { searchUrl } from "../utils__urls";
import { useLemma } from "../composables__lemma";

import LemmaCard from "./Component__Lemma_Card.vue";

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

const { lemmiStore, onSelectLemma } = useLemma();

const isLoading = ref(false);

const resultIsReady = ref(false);

const lemmi = ref([]);

const onSubmitForm = async ({ lemma, isExactSearch }, { setErrors }) => {
  try {
    resultIsReady.value = false;
    const url = `${searchUrl}/${lemma}?${new URLSearchParams({
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
</script>
