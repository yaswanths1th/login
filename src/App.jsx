import React from "react";
import { Routes, Route } from "react-router-dom";
import Sidebar from "./components/Sidebar";
import HeaderBar from "./components/HeaderBar";
import Dashboard from "./components/Dashboard";

function Placeholder({title}) {
  return <div style={{paddingTop:24}}><h2>{title}</h2><p style={{marginTop:8}}>This page is a placeholder for the <b>{title}</b> route.</p></div>;
}

export default function App(){
  return (
    <div className="app">
      <Sidebar />
      <main className="main">
        <HeaderBar />
        <div style={{ paddingTop: 12 }}>
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/users" element={<Placeholder title="Manage Users" />} />
            <Route path="/registrations" element={<Placeholder title="Registrations" />} />
            <Route path="/settings" element={<Placeholder title="Settings" />} />
            <Route path="/reports" element={<Placeholder title="Reports" />} />
            <Route path="*" element={<Dashboard />} />
          </Routes>
        </div>
      </main>
    </div>
  );
}
