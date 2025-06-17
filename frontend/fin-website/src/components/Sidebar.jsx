import { useState } from "react";
import "./Sidebar.css";
import { Link } from "react-router-dom";
import { MdSpaceDashboard, MdPieChart } from "react-icons/md";

function Sidebar() {
  return (
    <div className="sidebar">
      <div className="sidebar-header">
        <h2>RCB</h2>
      </div>
      <div className="sidebar-content">
        <ul>
          <li>
            <span>
              <MdSpaceDashboard fontSize={24}/>
              <Link to="/" className="sidebar-link">Dashboard</Link>
            </span>
          </li>
          <li>
            <span>
              <MdPieChart fontSize={24}/>
              <Link to="/about" className="sidebar-link">Portfolios</Link>
            </span>
          </li>
        </ul>
      </div>
    </div>
  );
}

export default Sidebar;
