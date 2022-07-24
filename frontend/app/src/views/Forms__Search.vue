<template>
  <Form
    v-slot="{ errors, isSubmitting, values: { lemma } }"
    :validation-schema="validationSchema"
    @submit="onSearchLemma"
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
        <Field v-slot="{ field }" name="exact" type="checkbox" :value="true">
          <label>
            <input type="checkbox" name="exact" v-bind="field" :value="true" />
            <span class="hast-text-gray"> effettua ricerca esatta </span>
          </label>
        </Field>
        <div class="has-text-danger">
          {{ errors.exact }}
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
</template>

<script setup>
/* eslint-disable no-unused-vars */
import { ref, watch, onMounted } from "vue";
import { configure, Form, Field } from "vee-validate";
import { boolean, object, string } from "yup";

const props = defineProps({
  resultIsReady: {
    type: Boolean,
    default: false,
  },
});

const emit = defineEmits({
  "on-search-lemma": (value) => {
    const c1 = Object.keys(value).every((key) =>
      ["formData", "searchType", "setErrors"].includes(key)
    );
    const c2 = Object.keys(value.formData).every((key) =>
      ["lemma", "exact"].includes(key)
    );
    return c1 && c2;
  },
});

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
  exact: boolean(),
});

const isLoading = ref(false);

watch(
  () => props.resultIsReady,
  (value) => {
    if (value) isLoading.value = false;
  }
);

const searchType = ref("SearchLemmi");

const onSearchLemma = async ({ lemma, exact }, { setErrors }) => {
  emit("on-search-lemma", {
    formData: {
      lemma,
      exact: exact || false,
    },
    searchType: searchType.value,
    setErrors,
  });
};

const onInvalidSubmitForm = () => {
  isLoading.value = false;
};

onMounted(() => {
  const lemmaInput = document.getElementsByTagName("input")[0];
  lemmaInput.focus();
});
</script>
