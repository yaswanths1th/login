import React, { useState } from "react";
import "./App.css";

function App() {
  // mock user data
  const [user, setUser] = useState({
    name: "MAHENDRA",
    phone: "7845637474",
    email: "mahi@gmail.com",
    house: "3nd Floor",
    street: "Bank Street",
    landmark: "Near Hdfc",
    area: "Koti",
    district: "Rangareddy",
    state: "Telangana",
    country: "India",
    pincode: "500001",
  });

  const [isEditing, setIsEditing] = useState(false);
  const [tempUser, setTempUser] = useState({ ...user });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setTempUser({ ...tempUser, [name]: value });
  };

  const handleSave = () => {
    setUser({ ...tempUser });
    setIsEditing(false);
  };

  return (
    <div className="container">
      {/* Header */}
      <header className="header">
        <h2>User Details</h2>
        <button
          className="edit-btn"
          onClick={() => setIsEditing((prev) => !prev)}
        >
          {isEditing ? "Cancel" : "Edit Details"}
        </button>
      </header>

      {/* Profile Information */}
      <section className="profile-info">
        <h3>Profile Information</h3>

        {/* Personal Details */}
        <div className="card">
          <h4>Personal Details</h4>
          <div className="grid">
            <div className="field">
              <label>Name</label>
              {isEditing ? (
                <input
                  name="name"
                  value={tempUser.name}
                  onChange={handleChange}
                />
              ) : (
                <p>{user.name}</p>
              )}
            </div>

            <div className="field">
              <label>Phone Number</label>
              {isEditing ? (
                <input
                  name="phone"
                  value={tempUser.phone}
                  onChange={handleChange}
                />
              ) : (
                <p>{user.phone}</p>
              )}
            </div>

            <div className="field">
              <label>Email</label>
              {isEditing ? (
                <input
                  name="email"
                  value={tempUser.email}
                  onChange={handleChange}
                />
              ) : (
                <p>{user.email}</p>
              )}
            </div>
          </div>
        </div>

        {/* Address Details */}
        <div className="card">
          <h4>Address Details</h4>
          <div className="grid">
            <div className="field">
              <label>House/Flat.No</label>
              {isEditing ? (
                <input
                  name="house"
                  value={tempUser.house}
                  onChange={handleChange}
                />
              ) : (
                <p>{user.house}</p>
              )}
            </div>

            <div className="field">
              <label>Street</label>
              {isEditing ? (
                <input
                  name="street"
                  value={tempUser.street}
                  onChange={handleChange}
                />
              ) : (
                <p>{user.street}</p>
              )}
            </div>

            <div className="field">
              <label>Landmark</label>
              {isEditing ? (
                <input
                  name="landmark"
                  value={tempUser.landmark}
                  onChange={handleChange}
                />
              ) : (
                <p>{user.landmark}</p>
              )}
            </div>

            <div className="field">
              <label>Area</label>
              {isEditing ? (
                <input
                  name="area"
                  value={tempUser.area}
                  onChange={handleChange}
                />
              ) : (
                <p>{user.area}</p>
              )}
            </div>

            <div className="field">
              <label>District</label>
              {isEditing ? (
                <input
                  name="district"
                  value={tempUser.district}
                  onChange={handleChange}
                />
              ) : (
                <p>{user.district}</p>
              )}
            </div>

            <div className="field">
              <label>State</label>
              {isEditing ? (
                <input
                  name="state"
                  value={tempUser.state}
                  onChange={handleChange}
                />
              ) : (
                <p>{user.state}</p>
              )}
            </div>

            <div className="field">
              <label>Country</label>
              {isEditing ? (
                <input
                  name="country"
                  value={tempUser.country}
                  onChange={handleChange}
                />
              ) : (
                <p>{user.country}</p>
              )}
            </div>

            <div className="field">
              <label>Pincode</label>
              {isEditing ? (
                <input
                  name="pincode"
                  value={tempUser.pincode}
                  onChange={handleChange}
                />
              ) : (
                <p>{user.pincode}</p>
              )}
            </div>
          </div>
        </div>

        {isEditing && (
          <button className="save-btn" onClick={handleSave}>
            Save Changes
          </button>
        )}
      </section>
    </div>
  );
}

export default App;
