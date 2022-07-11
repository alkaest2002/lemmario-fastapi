<template>
  <div class="card my-2 is-clickable" @click="emit('update:modelValue', lemma.rowid)">
    <div class="card-content">
      <p class="is-size-5 has-text-weight-bold">
        {{ lemma.lemma }}
      </p>
      <p :class="{ 'is-expanded': isExpanded}">
        {{ lemma.definition }}
      </p>
    </div>
  </div>
</template>

<script setup>
 /* eslint-disable no-unused-vars */
 import { computed } from "vue";

const emit = defineEmits({
  "update:modelValue": value => typeof value == "number"
})

const props = defineProps({
  modelValue: {
    type: Number,
    default: null
  },

  lemma: {
    type: Object,
    required: true,
  }
});

const isExpanded = computed(() => props.modelValue == props.lemma.rowid)

</script>

<style lang="scss" scoped>
  .card-content {
    
    > p:nth-child(2) {
      height: 50px;
      overflow: hidden;
      text-overflow: ellipsis;

      &.is-expanded {
        height: 100%;
      }
    }   
  }
</style>