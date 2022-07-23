<template>
  <div>
   <base-title>Modifica</base-title>
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
        <div class="buttons are-medium">
          <button
            class="button is-primary"
            @click="$router.go(-1)"
          >
             &larr;
          </button>
          <base-loading-button
            v-model="isLoading"
            :type="'submit'"
            :button-css="'is-info'"
            :disabled="isSubmitting || !(lemma && definition)"
          >
            {{ selectedLemma.rowid ? 'Modifica' : 'Inserisci' }}
          </base-loading-button>
          <base-loading-button
            v-model="isLoading"
            :button-css="'is-danger'"
            :disabled="isSubmitting || !(lemma && definition)"
            @click="onDeleteLemma"
          >
            Elimina
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
import { useRoute } from "vue-router";
import { configure, Form, Field } from "vee-validate";
import { object, string } from "yup";

import { useLemmiStore } from "../store__lemmi";
import { fetchWrapper } from "../utils__fetch";
import { insertUrl, editUrl, deleteUrl } from "../utils__urls";
import { router } from "../router__main";

const lemmiStore = useLemmiStore();

const { post, put, del } = fetchWrapper;

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

const route = useRoute();

let selectedLemma = lemmiStore.currentSelectedLemma;

const isLoading = ref(false);

const onSubmitForm = async (payload, { setErrors }) => {
  try {
    const upsertUrl = selectedLemma.rowid
      ? `${editUrl}/${selectedLemma.rowid}`
      : insertUrl
    const restOp = selectedLemma.rowid
      ? put
      : post
    const lemmaToUpsert = await restOp(upsertUrl, { payload });
    lemmiStore.updateLemma(lemmaToUpsert);
    router.push({
      name: "route-list",
      query: { scroll: route.query.scroll },
    });
  } catch (error) {
    setErrors({ apiError: error });
  } finally {
    isLoading.value = false;
  }
};

const onDeleteLemma = async (_, { setErrors }) => {
  try {
    await del(`${deleteUrl}/${selectedLemma.rowid}`);
  } catch (error) {
    setErrors({ apiError: error });
  } finally {
    isLoading.value = false;
  }
};

onMounted(() => {
  const el = document.getElementsByTagName("textarea")[0];
  el.style.height = `${el.scrollHeight + 20}px`;
});
</script>
