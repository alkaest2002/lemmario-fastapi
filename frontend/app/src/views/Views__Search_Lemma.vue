<template>
  <div>
    <h2 class="is-size-2 has-text-weight-bold mb-6">Cerca</h2>
    <Form
      v-slot="{ errors, isSubmitting, values: { lemma } }"
      :validation-schema="validationSchema"
      @submit="onSubmitForm"
    >
      <div class="field">
        <div class="control">
          <Field
            name="lemma"
            type="text"
            class="input is-medium"
            placeholder="lemma da cercare"
            :class="{ 'is-danger': errors.lemma }"
          />
          <div class="has-text-danger">
            {{ errors.lemma }}
          </div>
        </div>
      </div>
      <div class="field">
        <div class="control">
          <Field v-slot="{ field }" name="isExactSearch" type="checkbox" :value="true">
            <label>
              <input type="checkbox" name="isExactSearch" v-bind="field" :value="true">
              Ricerca esatta
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
    <div v-if="result.length > 0" class="mt-5">
      <div class="is-flex is-flex-direction-column is-justify-content-center">
        <div v-for="(lemma, index) in result" :key="index" class="card my-2">
          <div class="card-content">
            <p v-html="lemma.definition" />
          </div>
        </div>
      </div>
    </div>
    <div v-if="result.length == 0 && resultIsReady" class="mt-5">
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

configure({
  validateOnBlur: false,
  validateOnChange: true,
  validateOnInput: false,
  validateOnModelUpdate: true,
});

const validationSchema = object().shape({
  lemma: string().required("lemma richiesto"),
  isExactSearch: boolean(),
});

const { get } = fetchWrapper;

const isLoading = ref(false);

const resultIsReady = ref(false);

const result = ref([]);

const onSubmitForm = async ({ lemma, isExactSearch }, { setErrors }) => {
  try {
    resultIsReady.value = false;
    const url = `${searchUrl}/${lemma}?${new URLSearchParams({isExactSearch: isExactSearch || false })}`
    result.value = await get(url);
    resultIsReady.value = true;
  } catch (error) {
    setErrors({ apiError: error });
  } finally {
    isLoading.value = false;
  }
};
</script>
