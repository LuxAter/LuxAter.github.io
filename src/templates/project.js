import React from "react"
import { graphql } from "gatsby"
import { FaGithub } from 'react-icons/fa';
// import rehypeReact from "rehype-react"

import Layout from "../layouts/index"
import { Breadcrumb } from "../components/typeogrophy"
import { Row, Column} from "../components/grid"
// import { Plotly, LazyPlot } from "../components/plotly"

// const renderAst = new rehypeReact({
  // createElement: React.createElement,
  // components: {
    // "lazyplot": LazyPlot,
    // "plotly": Plotly,
  // }
// }).Compiler;

export default function Template({data,}) {
    const { markdownRemark } = data
    const { frontmatter, html, timeToRead } = markdownRemark
    return (
        <Layout>
            <Breadcrumb path={frontmatter.path}/>
            <Row>
                <Column width="nine">
                    <h1>{frontmatter.title}</h1>
                    <p className="page-subheader">{frontmatter.date} {timeToRead}m</p>
                </Column>
                <Column width="three">
    { (frontmatter.github !== null) ? <a href={frontmatter.github}><FaGithub size="3rem"/></a> : <div></div> }
    { (frontmatter.tags !== null) ? <ul className="tags">{frontmatter.tags.map((tag) => {
        return (<li className="tag" key={tag}>{tag}</li>)
    })}</ul> : <ul></ul>}
                </Column>
            </Row>
            <div dangerouslySetInnerHTML={{__html: html}} />
        </Layout>
    )
}
export const pageQuery = graphql`
    query($path: String!) {
        markdownRemark(frontmatter: {path: {eq: $path}}) {
            html
            timeToRead
            frontmatter {
                date(formatString: "MMMM DD, YYYY")
                path
                title
                tags
                github
            }
        }
    }
`
