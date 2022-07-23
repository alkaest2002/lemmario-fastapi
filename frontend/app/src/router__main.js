import { createRouter, createWebHistory } from "vue-router";

import { useAuthStore } from "./store__auth";
import LoginView from "./views/Views__Login.vue";
import ListView from "./views/Views__List.vue";
import UpsertView from "./views/Views__Upsert.vue";
import SearchView from "./views/Views__Search.vue";

export const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  linkActiveClass: "active",
  routes: [
    { name: "route-list", path: "/", component: ListView },
    { name: "route-upsert", path: "/upsert/", component: UpsertView },
    { name: "route-search", path: "/search", component: SearchView },
    { name: "route-login", path: "/login", component: LoginView },
  ],
});

router.beforeEach(async (to) => {
  const auth = useAuthStore();
  const publicRoutes = ["route-login"];
  const authRequired = !publicRoutes.includes(to.name);
  if (!authRequired && auth.isLoggedIn) return { name: "route-list" };
  if (authRequired && !auth.isLoggedIn) {
    auth.returnUrl = to.fullPath;
    return { name: "route-login" };
  }
});
