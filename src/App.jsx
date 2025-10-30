import React from "react";
import { Link } from "react-router-dom";

export default function App() {
  return (
    <div>
      <h1>Welcome</h1>
      <p><Link to="/address">Go to address form</Link></p>
    </div>
  );
}
