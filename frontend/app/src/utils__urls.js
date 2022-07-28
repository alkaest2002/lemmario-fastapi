const baseUrl = import.meta.env.VITE_API_URL;

export const authUrl = `${baseUrl}/utenti/login`;
export const lemmiUrl = `${baseUrl}/lemmi`;
export const insertUrl = `${baseUrl}/lemmi/insert`;
export const editUrl = `${baseUrl}/lemmi/update`;
export const deleteUrl = `${baseUrl}/lemmi/delete`;
export const searchUrl = `${baseUrl}/lemmi/search`;
export const searchUrlTreccani = `${baseUrl}/treccani/search`;
export const searchUrlOlivetti = `${baseUrl}/olivetti/search`;
