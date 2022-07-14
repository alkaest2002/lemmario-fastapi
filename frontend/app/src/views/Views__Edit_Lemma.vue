<template>
  <div>
    <h2 class="is-size-2 has-text-weight-bold mb-6">Modifica</h2>
    <Form
      v-slot="{ errors, isSubmitting, values: { lemma, definition } }"
      :validation-schema="validationSchema"
      :initial-values="selectedLemma"
      @submit="onSubmitForm"
    >
      <div class="field">
        <label class="label">Lemma</label>
        <div class="control">
          <Field
            name="lemma"
            type="text"
            class="input is-medium"
            placeholder="lemma"
            :class="{ 'is-danger': errors.lemma }"
          />
          <div class="has-text-danger">
            {{ errors.lemma }}
          </div>
        </div>
      </div>
      <div class="field">
        <label class="label">Definizione lemma</label>
        <div class="control">
          <Field
            as="textarea"
            name="definition"
            class="input is-medium"
            placeholder="Definizione lemma"
            :class="{ 'is-danger': errors.definition }"
          />
          <div class="has-text-danger">
            {{ errors.definition }}
          </div>
        </div>
      </div>
      <div class="control mt-5">
        <div class="buttons">
          <base-loading-button
            v-model="isLoading"
            :type="'submit'"
            :button-css="'is-medium is-info'"
            :disabled="isSubmitting || !(lemma && definition)"
          >
            Modifica lemma
          </base-loading-button>
          <base-loading-button
            v-model="isLoading"
            :button-css="'is-medium is-danger'"
            :disabled="isSubmitting || !(lemma && definition)"
            @click="onDeleteLemma"
          >
            Elimina lemma
          </base-loading-button>
        </div>
      </div>
      <div v-if="errors.apiError" class="has-text-danger mt-3 mb-0">
        {{ errors.apiError }}
      </div>
    </Form>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { configure, Form, Field } from "vee-validate";
import { object, string } from "yup";

import { fetchWrapper } from "../utils__fetch";
import { useLemmiStore } from "../store__lemmi";

const lemmiStore = useLemmiStore();

const baseUrl = import.meta.env.VITE_API_URL;
const editUrl = `${baseUrl}/lemmi/update`;

const { put } = fetchWrapper;

configure({
  validateOnBlur: false,
  validateOnChange: true,
  validateOnInput: false,
  validateOnModelUpdate: true,
});

const validationSchema = object().shape({
  lemma: string().required("lemma richiesto"),
  definition: string().required("definizione richiesta"),
});

let selectedLemma = lemmiStore.currentSelectedLemma;

const isLoading = ref(false);

const onSubmitForm = async ({ lemma, definition }, { setErrors }) => {
  try {
    const payload = { lemma, definition };
    await put(`${editUrl}/${selectedLemma.rowid}`, { payload });
  } catch (error) {
    setErrors({ apiError: error });
  } finally {
    isLoading.value = false;
  }
};

const onDeleteLemma = () => {
  isLoading.value = false;
};

onMounted(() => {
  const el = document.getElementsByTagName("textarea")[0];
  el.style.height = `${el.scrollHeight + 20}px`;
});
</script>
