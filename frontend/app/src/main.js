import { createApp } from "vue";
import { createPinia } from "pinia";

import { router } from "./router__main";
import BaseLayout from "./views/Layouts__Base.vue";
import BaseLoadingButton from "./views/components/BASE__loading_button.vue";

import "../node_modules/bulma/css/bulma.css";
import App from "./App.vue";

const app = createApp(App);

app.use(createPinia()).use(router);

app.component("BaseLayout", BaseLayout);
app.component("BaseLoadingButton", BaseLoadingButton);

app.mount("#app");
