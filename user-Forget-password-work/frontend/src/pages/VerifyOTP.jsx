// src/pages/VerifyOTP.jsx
import React, { useState } from "react";
import axios from "axios";
import { toast } from "react-toastify";
import { useLocation, useNavigate } from "react-router-dom";
import "../styles/styles.css";

function VerifyOTP() {
  const [otp, setOtp] = useState("");
  const [newPassword, setNewPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const location = useLocation();
  const navigate = useNavigate();

  const email = location.state?.email || "";

  const handleVerifyOTP = async (e) => {
    e.preventDefault();

    if (!otp || !newPassword || !confirmPassword) {
      toast.error("All fields are required.");
      return;
    }

    if (newPassword !== confirmPassword) {
      toast.error("Passwords do not match!");
      return;
    }

    try {
      const response = await axios.post("http://127.0.0.1:8000/api/verify-otp/", {
        email,
        otp,
        new_password: newPassword,
        confirm_password: confirmPassword,
      });

      toast.success(response.data.message || "Password reset successful!");
      navigate("/login");
    } catch (error) {
      toast.error(error.response?.data?.error || "Invalid OTP or request");
    }
  };

  return (
    <div className="auth-container">
      <form className="auth-card" onSubmit={handleVerifyOTP}>
        <h2 className="auth-title">Verify OTP</h2>
        <p className="auth-subtitle">Enter OTP and reset your password</p>

        <div className="form-group">
          <label>OTP</label>
          <input
            type="text"
            placeholder="Enter 6-digit OTP"
            value={otp}
            onChange={(e) => setOtp(e.target.value)}
            required
          />
        </div>

        <div className="form-group">
          <label>New Password</label>
          <input
            type="password"
            placeholder="Enter new password"
            value={newPassword}
            onChange={(e) => setNewPassword(e.target.value)}
            required
          />
        </div>

        <div className="form-group">
          <label>Confirm Password</label>
          <input
            type="password"
            placeholder="Re-enter new password"
            value={confirmPassword}
            onChange={(e) => setConfirmPassword(e.target.value)}
            required
          />
        </div>

        <button type="submit" className="btn-primary">
          Reset Password
        </button>
      </form>
    </div>
  );
}

export default VerifyOTP;
