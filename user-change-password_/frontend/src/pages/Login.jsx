// src/pages/Login.jsx
import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { loginUser } from "../api";

const Login = () => {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");

    try {
      await loginUser(username, password);
      alert("Login Successful!");
      navigate("/change-password");
    } catch (err) {
      setError(err.message);
    }
  };

  return (
    <div
      style={{
        height: "100vh",
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        flexDirection: "column",
        background: "linear-gradient(135deg, #d9e7ff, #f3f7ff)",
      }}
    >
      <form
        onSubmit={handleSubmit}
        style={{
          background: "white",
          padding: "30px 40px",
          borderRadius: "15px",
          boxShadow: "0 4px 20px rgba(0, 0, 0, 0.1)",
          width: "350px",
        }}
      >
        <h2 style={{ textAlign: "center", color: "#2563eb", marginBottom: "20px" }}>Login</h2>

        <label>Username</label>
        <input
          type="text"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          placeholder="Enter username"
          required
          style={{
            width: "100%",
            padding: "10px",
            marginTop: "5px",
            border: "1px solid #cbd5e1",
            borderRadius: "8px",
            marginBottom: "15px",
          }}
        />

        <label>Password</label>
        <input
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          placeholder="Enter password"
          required
          style={{
            width: "100%",
            padding: "10px",
            marginTop: "5px",
            border: "1px solid #cbd5e1",
            borderRadius: "8px",
            marginBottom: "15px",
          }}
        />

        {error && (
          <p style={{ color: "red", fontSize: "14px", marginBottom: "10px" }}>
            {error}
          </p>
        )}

        <button
          type="submit"
          style={{
            width: "100%",
            backgroundColor: "#2563eb",
            color: "white",
            padding: "12px",
            border: "none",
            borderRadius: "8px",
            fontWeight: "bold",
            cursor: "pointer",
            transition: "0.3s",
          }}
        >
          Login
        </button>
      </form>
    </div>
  );
};

export default Login;
