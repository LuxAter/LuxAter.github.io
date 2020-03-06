import React from "react";

import { Link, graphql } from "gatsby"
import Img from "gatsby-image"
import { FaGithub } from 'react-icons/fa';

import Layout from "../layouts/list"
import { Section, Breadcrumb } from "../components/typeogrophy"
import { Row, Column } from "../components/grid"

export default function Index({ data }) {
    const { edges: posts } = data.allMarkdownRemark
    return (
        <Layout>
            <Breadcrumb path="/projects"/>
            {posts
                .filter(post => post.node.frontmatter.title.length > 0)
                .map(({ node: post }) => {
                    let excerpt = null
                    if (post.frontmatter.featuredImage !== null) {
                        excerpt = (<Row>
                            <Column width="three">
                                <Img fluid={post.frontmatter.featuredImage.childImageSharp.fluid} />
                            </Column>
                            <Column width="nine">
                                {post.excerpt}
                            </Column>
                        </Row>)
                    } else {
                        excerpt = post.excerpt
                    }
                    return (
                        <Section id={post.id} key={post.id}>
                            <Row>
                                <Column width="nine">
                                    <Link className="page-link" to={post.frontmatter.path}>{post.frontmatter.title}</Link>
                                    <p className="page-subheader">{post.frontmatter.date} {post.timeToRead}m</p>
                                </Column>
                                <Column width="three">
                                    { (post.frontmatter.github !== null) ? <a href={post.frontmatter.github}><FaGithub size="3rem"/></a> : <div></div>}
                                    { (post.frontmatter.tags !== null) ? <ul className="tags">{post.frontmatter.tags.map((tag) => {
                                        return (<li className="tag" key={tag}>{tag}</li>)
                                    })}</ul> : <ul></ul>}
                                </Column>
                            </Row>
                            <div>
                                {excerpt}
                            </div>
                        </Section>
                    )
                })}
        </Layout>
    )
}

export const pageQuery = graphql`
    query {
        allMarkdownRemark(sort: { order: DESC, fields: [frontmatter___date]}) {
            edges {
                node {
                    timeToRead
                    excerpt(pruneLength: 250)
                    id
                    frontmatter {
                        title
                        date(formatString: "MMMM DD, YYYY")
                        path
                        github
                        tags
                        featuredImage {
                            childImageSharp {
                                fluid {
                                    ...GatsbyImageSharpFluid
                                }
                            }
                        }
                    }
                }
            }
        }
    }
`