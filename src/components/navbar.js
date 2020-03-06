import React from 'react'
import { Link } from 'gatsby'


export const NavbarBrand = (params) => (
  <li className="navbar-item">
    <Link className="navbar-link" to="/">
      {params.children}
    </Link>
  </li>
)

export const NavbarLink = (params) => (
  <li className="navbar-item">
    <Link className="navbar-link" to={params.to}>
      {params.children}
    </Link>
  </li>
)

export const Navbar = ({ children }) => (
  <nav className="navbar">
    <div className="container">
      <ul className="navbar-list">
        {children}
      </ul>
    </div>
  </nav>
)
