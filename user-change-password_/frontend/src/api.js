// src/api.js
const BASE_URL = "http://127.0.0.1:8000";

export async function loginUser(username, password) {
  try {
    const response = await fetch(`${BASE_URL}/api/token/`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username, password }),
    });

    if (!response.ok) {
      throw new Error("Invalid username or password");
    }

    const data = await response.json();

    // Store JWT tokens in localStorage
    localStorage.setItem("access_token", data.access);
    localStorage.setItem("refresh_token", data.refresh);

    return data;
  } catch (error) {
    throw error;
  }
}
