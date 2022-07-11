import { defineStore } from "pinia";
import { fetchWrapper } from "./utils__fetch";

const baseUrl = import.meta.env.VITE_API_URL;
const lemmiUrl = `${baseUrl}/lemmi/`;
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
    async load_data() {
      try {
        const payload = await get(lemmiUrl);
        this.state = payload;
        return Promise.resolve(true);
      } catch (error) {
        return Promise.reject(error);
      }
    },
  },
});
