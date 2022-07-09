import { useAuthStore } from "./store__auth";

const request = (method) =>
  async (url, body, isformUrlEncoded=true) => {
    const requestOptions = { method, headers: authHeader(url)};
    if (body) {
      if (isformUrlEncoded) {
        requestOptions.headers["Content-Type"] = "application/x-www-form-urlencoded";
        requestOptions.body = new URLSearchParams({...body});
      } else{
        requestOptions.headers["Content-Type"] = "application/json";
        requestOptions.body = body;
      }
    }
    const response = await fetch(url, requestOptions);
    return handleResponse(response);
  }


const authHeader = (url) => {
  const auth  = useAuthStore();
  const isApiUrl = url.startsWith(import.meta.env.VITE_API_URL);
  return auth.isLoggedIn && isApiUrl 
    ? { Authorization: `Bearer ${auth.token}` }
    : {};
}

const handleResponse = async (response) => {
  const data = await response.json();
  if (!response.ok) {
    const { token, logout } = useAuthStore();
    if ([401, 403].includes(response.status) && token) logout();
    return Promise.reject(data?.detail || response.statusText || "error");
  }
  return data;
}

export const fetchWrapper = {
  get: request("GET"),
  post: request("POST"),
  put: request("PUT"),
  delete: request("DELETE")
};