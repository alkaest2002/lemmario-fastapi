const baseUrl = import.meta.env.VITE_API_URL;

export const authUrl = `${baseUrl}/utenti/login`;
export const lemmiUrl = `${baseUrl}/lemmi`;
export const editUrl = `${baseUrl}/lemmi/update`;
export const deleteUrl = `${baseUrl}/lemmi/delete`;
