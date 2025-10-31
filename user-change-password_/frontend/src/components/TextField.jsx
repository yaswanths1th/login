import React from "react";

export default function TextField({ label, type = "text", value, onChange, placeholder }) {
  return (
    <div className="tf">
      <label className="tf-label">{label}</label>
      <input
        className="tf-input"
        type={type}
        value={value}
        onChange={onChange}
        placeholder={placeholder}
      />
    </div>
  );
}
