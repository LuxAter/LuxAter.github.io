import React from "react"

import { Navbar, NavbarBrand, NavbarLink } from "../components/navbar"


export default ({children}) => {
    return (
        <div className="container">
            <Navbar>
                <NavbarBrand>Arden Rasmussen</NavbarBrand>
                <NavbarLink to="/projects">Projects</NavbarLink>
            </Navbar>
            {children}
        </div>
    )
}