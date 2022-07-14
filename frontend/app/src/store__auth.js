import { defineStore } from "pinia";
import { fetchWrapper } from "./utils__fetch";
import { authUrl } from "./utils__urls";

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
        const data = {
          payload: { username, password },
          typeOfPayload: "formUrlEncoded",
        };
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
