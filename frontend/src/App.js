// App.js
import React from "react";
import PopupOperation from "./components/PopupOperation";
import { Route, Routes } from "react-router-dom";
import FinancialTableSimulation from "./components/FinancialTableSimulation";

function App() {
  return (
    <div className="bg-white min-h-screen">
      <Routes>
        <Route path="/" element={<PopupOperation />} />
        <Route path="/financialtable " element={<FinancialTableSimulation />} />
      </Routes>
    </div>
  );
}

export default App;
