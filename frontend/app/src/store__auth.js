import { defineStore } from "pinia";

import { fetchWrapper } from "./utils__fetch";

const baseUrl = import.meta.env.VITE_API_URL;
const authUrl = `${baseUrl}/utenti/login`;
const accessToken = localStorage.getItem("accessToken");

export const useAuthStore = defineStore({
  id: "auth",

  state: () => ({
    accessToken: accessToken ? JSON.parse(accessToken) : null,
    returnUrl: null,
  }),

  getters: {
    isLoggedIn: (state) => state.accessToken != null,
  },

  actions: {
    async login(username, password) {
      try {
        const { access_token: accessToken } = await fetchWrapper.post(
          authUrl,
          useAuthStore(),
          { body: { username, password }, isformUrlEncoded: true }
        );
        this.accessToken = accessToken;
        localStorage.setItem("accessToken", JSON.stringify(accessToken));
        return Promise.resolve(true);
      } catch (error) {
        return Promise.reject(error);
      }
    },

    logout() {
      this.accessToken = null;
      localStorage.removeItem("accessToken");
      return Promise.resolve(true);
    },
  },
});
