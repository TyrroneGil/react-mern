import { useState } from "react";
import { Outlet, NavLink } from "react-router-dom";

export default function NavigationBar() {
  const [openNav, setOpenNav] = useState(false);

  return (
    <div className="flex flex-col w-screen h-screen overflow-hidden">
      {/* Top Bar */}
      <div className="w-full text-white h-[10%] bg-blue-900 flex items-center px-4">
        <button onClick={() => setOpenNav(true)}>Open</button>
      </div>

      <div className="flex h-[90%] relative">
        {/* Sidebar */}
        <div
          className={`absolute left-0 top-0 h-full bg-slate-100
          transition-all duration-300 ease-in-out
          ${openNav ? "w-[20%] translate-x-0" : "w-[20%] -translate-x-full"}`}
        >
          <button onClick={() => setOpenNav(false)}>X</button>
          <nav className="flex flex-col gap-2 p-4">
            <NavLink to="/" className={({ isActive }) =>
    isActive ? "font-bold text-blue-600" : ""
  }>Home</NavLink>
            <NavLink to="/about" className={({ isActive }) =>
    isActive ? "font-bold text-blue-600" : ""
  }>About</NavLink>
          </nav>
        </div>

        {/* Main Content */}
        <div
          className={`h-full bg-slate-400 transition-all duration-300 ease-in-out
          ${openNav ? "w-[80%] ml-[20%]" : "w-full ml-0"}`}
        >
          <Outlet /> {/* <-- Your pages render here */}
        </div>
      </div>
    </div>
  );
}
