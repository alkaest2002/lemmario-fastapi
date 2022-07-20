import { createApp } from "vue";
import { createPinia } from "pinia";

import { router } from "./router__main";
import BaseLayout from "./views/Base__Layout.vue";
import BaseTitle from "./views/Base__Title.vue";
import BaseLoadingButton from "./views/Base__Loading_Button.vue";

import "../node_modules/bulma/css/bulma.css";
import "./assets/styles.css";

import App from "./App.vue";

const app = createApp(App);

app.use(createPinia()).use(router);

app.component("BaseLayout", BaseLayout);
app.component("BaseLoadingButton", BaseLoadingButton);
app.component("BaseTitle", BaseTitle);

app.mount("#app");
