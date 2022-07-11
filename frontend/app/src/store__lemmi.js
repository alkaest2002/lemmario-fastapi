import { defineStore } from "pinia";
import { fetchWrapper } from "./utils__fetch";

const baseUrl = import.meta.env.VITE_API_URL;
const lemmiUrl = `${baseUrl}/lemmi`;
const { get } = fetchWrapper;

export const useLemmiStore = defineStore({
  id: "lemmi",

  state: () => ({
    data: [],
		metadata: {
			filter_by: null,
			filter_value: null,
			order_by: "lemma",
			order_value: "ASC",
			page_dir: "NEXT",
			page_size: 10,
			offset: null,
    }
  }),

  actions: {
    async fetchLemmi() {
      const payload = Object.keys(this.metadata).reduce((acc, itr) => {
        if (this.metadata[itr])
          acc[itr] = this.metadata[itr];
        return acc
      }, {});
      try {
        const data = await get(`${lemmiUrl}/list`, { payload });
        this.$state = data;
        return Promise.resolve(true);
      } catch (error) {
        return Promise.reject(error);
      }
    },
  },
});
