// src/pages/ForgotPassword.jsx
import React, { useState } from "react";
import axios from "axios";
import { toast } from "react-toastify";
import { useNavigate } from "react-router-dom";
import "../styles/styles.css";

function ForgotPassword() {
  const [email, setEmail] = useState("");
  const navigate = useNavigate();

  const handleSendOTP = async (e) => {
    e.preventDefault();
    if (!email) {
      toast.error("Please enter your email address.");
      return;
    }

    try {
      const response = await axios.post("http://127.0.0.1:8000/api/send-otp/", { email });
      toast.success(response.data.message || "OTP sent successfully!");
      navigate("/verify-otp", { state: { email } });
    } catch (error) {
      toast.error(error.response?.data?.error || "Error sending OTP");
    }
  };

  return (
    <div className="auth-container">
      <form className="auth-card" onSubmit={handleSendOTP}>
        <h2 className="auth-title">User Details</h2>
        <p className="auth-subtitle">Enter your email to receive a 6-digit OTP</p>

        <div className="form-group">
          <label>Email address</label>
          <input
            type="email"
            placeholder="you@company.com"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
        </div>

        <button type="submit" className="btn-primary">
          Send OTP
        </button>
      </form>
    </div>
  );
}

export default ForgotPassword;
