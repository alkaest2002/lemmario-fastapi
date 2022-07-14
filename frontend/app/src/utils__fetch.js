import { useAuthStore } from "./store__auth";

const request =
  (method) =>
  async (url, data = null) => {
    // add authorization
    const requestOptions = { method, headers: authHeader(url) };
    // manage methods
    if (["POST", "PUT"].indexOf(method) > -1) {
      const { payload, typeOfPayload } = data;
      requestOptions.headers["Content-Type"] =
        typeOfPayload == "formUrlEncoded"
          ? "application/x-www-form-urlencoded"
          : "application/json";
      requestOptions.body =
        typeOfPayload == "formUrlEncoded"
          ? new URLSearchParams(payload)
          : JSON.stringify(payload);
    } 
    if (["GET", "DELETE"].indexOf(method) > -1) {
      if (data) {
        const queryParams = new URLSearchParams(data.payload);
        url = `${url}?${queryParams}`;
      }
    }
    try {
      const response = await fetch(url, requestOptions);
      return handleResponse(response);
    } catch (error) {
      return Promise.reject(error);
    }
  };

const authHeader = (url) => {
  const { accessToken, isLoggedIn } = useAuthStore();
  const isApiUrl = url.startsWith(import.meta.env.VITE_API_URL);
  return isLoggedIn && isApiUrl
    ? { Authorization: `Bearer ${accessToken}` }
    : {};
};

const handleResponse = async (response) => {
  const { accessToken, logout } = useAuthStore();
  const data = await response.json();
  if (!response.ok) {
    if ([401, 403].includes(response.status) && accessToken) logout();
    return Promise.reject(data?.detail || response.statusText || "error");
  }
  return data;
};

export const fetchWrapper = {
  get: request("GET"),
  post: request("POST"),
  put: request("PUT"),
  del: request("DELETE"),
};
