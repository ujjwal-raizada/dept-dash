import React from 'react';
import { BrowserRouter } from "react-router-dom";

import Routes from "./routes/index";

export default function App() {
  return (
    <div className="App">
      <BrowserRouter basename="/">
        <Routes />
      </BrowserRouter>
    </div>
  );
}
