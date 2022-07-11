<template>
  <div>
    <h2 class="is-size-2 has-text-weight-bold mb-4">Home</h2>
    {{ lemmi }}
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useLemmiStore } from "../store__lemmi";
import { fetchWrapper } from "../utils__fetch";

const { get } = fetchWrapper;
const baseUrl = import.meta.env.VITE_API_URL;
const lemmiUrl = `${baseUrl}/lemmi/list`;

const lemmiStore = useLemmiStore();
const lemmi = ref(null);

onMounted(async () => {
  const payload = Object.keys(lemmiStore.metadata).reduce((acc, itr) => {
    if (lemmiStore.metadata[itr])
      acc[itr] = lemmiStore.metadata[itr];
    return acc
  }, {});
  console.log(payload)
  const data = { payload };
  try {
    lemmi.value = await get(lemmiUrl, data)
  } catch(error) {
    console.log(error)
  }
});
</script>
