import React from 'react'
import {Link} from 'gatsby'

export const Section = ({id, children}) => (
    <div className="docs-section" id={id} key={id}>
        {children}
    </div>
)

export const Breadcrumb = ({path}) => {
    path = path.substring(1).split('/');
    return (<ul className="breadcrumb">
        <li><Link to="/">home</Link></li>
        {path.map((pt, index) => {
        return (<li><Link to={path.slice(0, index+1).join('/')}>{pt}</Link></li>)
    })}</ul>)
}