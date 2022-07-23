import { useRouter } from "vue-router";
import { useLemmiStore } from "./store__lemmi";

export const useLemma = () => {
  /* eslint-disable no-unused-vars */

  const router = useRouter();

  const lemmiStore = useLemmiStore();

  const onSelectLemma = ({ lemma, isExpanded, isOverFlown }) => {
    lemmiStore.currentSelectedLemma = lemma;
    if ([isExpanded, !isExpanded && !isOverFlown].some(Boolean))
      router.push({
        name: "route-upsert",
        query: { scroll: window.pageYOffset },
      });
  };

  return {
    router,
    lemmiStore,
    onSelectLemma,
  };
};
