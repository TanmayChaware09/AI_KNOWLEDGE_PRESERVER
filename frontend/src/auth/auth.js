export function logout() {
  localStorage.removeItem("auth_token");
  localStorage.removeItem("token_type");
  localStorage.removeItem("auth_user");
  localStorage.removeItem("user_role");
  localStorage.removeItem("user_identifier");
  localStorage.removeItem("remember_me");

  window.location.href = "/";
}

export function getToken() {
  return localStorage.getItem("auth_token");
}

export function getUser() {
  const user = localStorage.getItem("auth_user");

  if (!user) {
    return null;
  }

  try {
    return JSON.parse(user);
  } catch {
    return null;
  }
}

export function isAuthenticated() {
  return Boolean(localStorage.getItem("auth_token"));
}