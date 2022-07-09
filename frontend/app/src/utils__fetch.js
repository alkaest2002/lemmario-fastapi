const request =
  (method) =>
  async (url, auth, data = null) => {
    const requestOptions = { method, headers: authHeader(url, auth) };
    if (data) {
      const { body, isformUrlEncoded } = data;
      requestOptions.headers["Content-Type"] = isformUrlEncoded
        ? "application/x-www-form-urlencoded"
        : "application/json";
      requestOptions.body = isformUrlEncoded ? new URLSearchParams(body) : body;
    }
    try {
      const response = await fetch(url, requestOptions);
      return handleResponse(response, auth);
    } catch (error) {
      return Promise.reject(error);
    }
  };

const authHeader = (url, auth) => {
  const isApiUrl = url.startsWith(import.meta.env.VITE_API_URL);
  return auth.isLoggedIn && isApiUrl
    ? { Authorization: `Bearer ${auth.accessToken}` }
    : {};
};

const handleResponse = async (response, auth) => {
  const data = await response.json();
  if (!response.ok) {
    if ([401, 403].includes(response.status) && auth.accessToken) auth.logout();
    return Promise.reject(data?.detail || response.statusText || "error");
  }
  return data;
};

export const fetchWrapper = {
  get: request("GET"),
  post: request("POST"),
  put: request("PUT"),
  delete: request("DELETE"),
};
