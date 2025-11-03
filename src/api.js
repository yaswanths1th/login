 import axios from "axios";

const API = axios.create({
  baseURL: "http://127.0.0.1:8000/api/registrations/",
  headers: {
    "Content-Type": "application/json",
  },
});

export async function fetchStats() {
  const res = await API.get("stats/");
  return res.data;
}

export async function fetchRegistrations() {
  const res = await API.get("");
  return res.data;
}

export async function createRegistration(payload) {
  const res = await API.post("", payload);
  return res.data;
}

