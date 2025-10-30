import React from "react";
import { createRoot } from "react-dom/client";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import App from "./App";
import AddressForm from "./components/AddressForm";

createRoot(document.getElementById("root")).render(
  <BrowserRouter>
    <Routes>
      <Route path="/" element={<App />} />
      <Route path="/address" element={<AddressForm initialUserId={1} />} />
      <Route path="/profile" element={<div>Profile / Dashboard (placeholder)</div>} />
    </Routes>
  </BrowserRouter>
);

