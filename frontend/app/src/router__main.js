import { createRouter, createWebHistory } from "vue-router";

import { useAuthStore } from "./store__auth";
import LoginView from "./views/Views__Login.vue";
import LemmiView from "./views/Views__Lemmi.vue";
import EditLemmaView from "./views/Views__Upsert_Lemma.vue";
import SearchLemmaView from "./views/Views__Search_Lemma.vue";

export const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  linkActiveClass: "active",
  routes: [
    { name: "route-list-lemmi", path: "/", component: LemmiView },
    { name: "route-upsert-lemma", path: "/upsert/", component: EditLemmaView },
    { name: "route-search-lemma", path: "/search", component: SearchLemmaView },
    { name: "route-login", path: "/login", component: LoginView },
  ],
});

router.beforeEach(async (to) => {
  const auth = useAuthStore();
  const publicRoutes = ["route-login"];
  const authRequired = !publicRoutes.includes(to.name);
  if (!authRequired && auth.isLoggedIn) return { name: "route-list-lemmi" };
  if (authRequired && !auth.isLoggedIn) {
    auth.returnUrl = to.fullPath;
    return { name: "route-login" };
  }
});
