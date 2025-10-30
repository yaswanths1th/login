import React, { useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";
import "../styles/address-form.css";

/* Config */
const GEOAPIFY_KEY = "cfbde6e6513242f68afce4e67a6595a3";
const API_BASE = "http://127.0.0.1:8000/api/addresses/"; // trailing slash required

/* Helpers */
const displayErrorMessage = (err) => (err ? <div className="error-message">⚠️ {err}</div> : null);

const validateHouseNo = (houseNo) => {
  if (!houseNo?.trim()) return { success: false, error: "Flat/House No is required" };
  if (houseNo.length > 64) return { success: false, error: "Max 64 characters allowed" };
  if (!/^[A-Za-z0-9\s\/\-\.,]+$/.test(houseNo)) return { success: false, error: "Invalid characters" };
  return { success: true };
};
const validateStreet = (street) => {
  if (!street?.trim()) return { success: false, error: "Street is required" };
  if (street.length > 128) return { success: false, error: "Max 128 characters allowed" };
  return { success: true };
};
const validateArea = (area) => {
  if (!area?.trim()) return { success: false, error: "Area is required" };
  return { success: true };
};
const validatePinCode = (pinCode) => {
  if (!pinCode?.trim()) return { success: false, error: "Pincode is required" };
  if (!/^\d{4,8}$/.test(pinCode)) return { success: false, error: "Invalid Pincode format" };
  return { success: true };
};

const fetchAutoLocation = async (pinCode) => {
  try {
    const url = `https://api.geoapify.com/v1/geocode/search?postcode=${encodeURIComponent(pinCode)}&format=json&apiKey=${GEOAPIFY_KEY}`;
    const res = await axios.get(url, { timeout: 8000 });
    const results = res.data?.features || res.data?.results || [];
    if (results.length > 0) {
      const info = results[0].properties || results[0];
      return {
        success: true,
        data: {
          country: info.country || "",
          state: info.state || info.region || "",
          district: info.county || info.city || info.state_district || "",
        },
      };
    }
    return { success: false, error: "No data found for this PIN code" };
  } catch (err) {
    console.error("Geoapify error:", err);
    return { success: false, error: "Failed to fetch location from Geoapify" };
  }
};

const submitAddress = async (payload) => {
  try {
    const res = await axios.post(API_BASE, payload, {
      headers: { "Content-Type": "application/json" },
      timeout: 10000,
    });
    return { success: true, data: res.data };
  } catch (err) {
    console.error("Submission Error:", err);
    const resp = err?.response?.data;
    if (resp) {
      if (resp.errors && typeof resp.errors === "object") {
        const messages = [];
        for (const [k, v] of Object.entries(resp.errors)) {
          if (Array.isArray(v)) messages.push(`${k}: ${v.join(", ")}`);
          else messages.push(`${k}: ${String(v)}`);
        }
        return { success: false, error: messages.join(" | ") };
      }
      if (resp.error) return { success: false, error: resp.error };
      if (resp.message) return { success: false, error: resp.message };
      return { success: false, error: JSON.stringify(resp) };
    }
    return { success: false, error: err.message || "Network or unknown error" };
  }
};

export default function AddressForm({ initialUserId }) {
  const [flatNo, setFlatNo] = useState("");
  const [street, setStreet] = useState("");
  const [landmark, setLandmark] = useState("");
  const [area, setArea] = useState("");
  const [pinCode, setPinCode] = useState("");
  const [country, setCountry] = useState("");
  const [state, setState] = useState("");
  const [district, setDistrict] = useState("");
  const [fieldErrors, setFieldErrors] = useState({});
  const [globalError, setGlobalError] = useState(null);
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handlePinBlur = async () => {
    const v = validatePinCode(pinCode);
    setFieldErrors((p) => ({ ...p, pinCode: v.success ? null : v.error }));
    if (!v.success) return;
    setLoading(true);
    const res = await fetchAutoLocation(pinCode);
    setLoading(false);
    if (res.success) {
      setCountry(res.data.country);
      setState(res.data.state);
      setDistrict(res.data.district);
      setFieldErrors((p) => ({ ...p, pinCode: null }));
    } else {
      setCountry("");
      setState("");
      setDistrict("");
      setFieldErrors((p) => ({ ...p, pinCode: res.error }));
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setGlobalError(null);

    const validations = {
      flatNo: validateHouseNo(flatNo),
      street: validateStreet(street),
      area: validateArea(area),
      pinCode: validatePinCode(pinCode),
    };
    const errors = Object.fromEntries(Object.entries(validations).map(([k, v]) => [k, v.success ? null : v.error]));
    setFieldErrors(errors);
    if (Object.values(errors).some(Boolean)) {
      setGlobalError("Please fix the highlighted errors.");
      return;
    }

    // ✅ Build JSON payload using user_id (NOT user)
    const payload = {
      user_id: initialUserId || 1, // 👈 Change 1 to your logged-in user's ID
      flat_no: flatNo,
      street,
      landmark,
      area,
      pincode: pinCode,
      country,
      state,
      district,
    };

    setLoading(true);
    const res = await submitAddress(payload);
    setLoading(false);

    if (res.success) {
      alert("✅ Address saved successfully!");
      navigate("/profile"); // adjust route as needed
    } else {
      setGlobalError(res.error);
    }
  };

  return (
    <form className="address-form" onSubmit={handleSubmit}>
      <h2>🏠 Add Address</h2>

      <label>Flat / House No</label>
      <input
        value={flatNo}
        onChange={(e) => setFlatNo(e.target.value)}
        onBlur={() => setFieldErrors((p) => ({ ...p, flatNo: validateHouseNo(flatNo).error }))}
      />
      {displayErrorMessage(fieldErrors.flatNo)}

      <label>Street</label>
      <input
        value={street}
        onChange={(e) => setStreet(e.target.value)}
        onBlur={() => setFieldErrors((p) => ({ ...p, street: validateStreet(street).error }))}
      />
      {displayErrorMessage(fieldErrors.street)}

      <label>Landmark (optional)</label>
      <input value={landmark} onChange={(e) => setLandmark(e.target.value)} />

      <label>Area</label>
      <input
        value={area}
        onChange={(e) => setArea(e.target.value)}
        onBlur={() => setFieldErrors((p) => ({ ...p, area: validateArea(area).error }))}
      />
      {displayErrorMessage(fieldErrors.area)}

      <label>Pincode</label>
      <input
        value={pinCode}
        onChange={(e) => setPinCode(e.target.value)}
        onBlur={handlePinBlur}
        placeholder="Enter PIN to auto-fill location"
      />
      {displayErrorMessage(fieldErrors.pinCode)}

      <label>Country</label>
      <input value={country} readOnly />

      <label>State</label>
      <input value={state} readOnly />

      <label>District</label>
      <input value={district} readOnly />

      {globalError && displayErrorMessage(globalError)}

      <button type="submit" disabled={loading}>
        {loading ? "Saving..." : "Save Address"}
      </button>
    </form>
  );
}
