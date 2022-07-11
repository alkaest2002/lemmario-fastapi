import { defineStore } from "pinia";
import { fetchWrapper } from "./utils__fetch";

const baseUrl = import.meta.env.VITE_API_URL;
const authUrl = `${baseUrl}/utenti/login`;

const { post } = fetchWrapper;

export const useAuthStore = defineStore({
  id: "auth",

  state: () => ({
    accessToken: null,
    returnUrl: null,
  }),

  getters: {
    isLoggedIn: (state) => state.accessToken != null,
  },

  actions: {
    async login(username, password) {
      try {
        const data = { payload: { username, password }, typeOfPayload: "formUrlEncoded" };
        const { access_token: accessToken } = await post(authUrl, data);
        this.accessToken = accessToken;
        return Promise.resolve(true);
      } catch (error) {
        return Promise.reject(error);
      }
    },

    logout() {
      this.accessToken = null;
      return Promise.resolve(true);
    },
  },
});
