import React from "react"

export const Grid = ({children}) => (
    <div className="container">
        {children}
    </div>
)

export const Row = ({children}) => (
    <div className="row">
        {children}
    </div>
)

export const Column = ({width,children}) => (
    <div className={width + ' columns'}>
        {children}
    </div>
)