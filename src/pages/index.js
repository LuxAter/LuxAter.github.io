import React from "react"
import { graphql} from 'gatsby'
import Img from 'gatsby-image'

import Layout from "../layouts/index"

import {Section} from "../components/typeogrophy"
import {Row, Column} from "../components/grid"

export default ({data}) => (
  <Layout>
    <Section id="aboutme">
      <h4>About Me</h4>
      <Row>
        <Column width="five">
          <p>
            <em>Arden Rasmussen</em> is currently an Undergraduate student at
            Lewis and Clark College, majoring in Mathematics & Computer
            Science, with a second major in Physics.
          </p>
          <p>
            My primary focus is on computer graphics. This includes real-time
            rendering and off-line rendering. There are several projects which
            demonstrate different rendering techniques, from ray tracing, to path
            tracing and ray marching, and using OpenGL for real-time physically
            based rendering.
          </p>
          <p>
            I also have a focus on building tools and libraries to be used in
            other more complex projects. The majority of these tools are aimed
            to be minimal, and easy to import into other projects. They range
            from profiling libraries, vector math libraries, and string formatting
            libraries. Specifics of these can be found in the projects tab.
          </p>
        </Column>
        <Column width="five">
          <Img fluid={data.file.childImageSharp.fluid} />
        </Column>
      </Row>
    </Section>
  </Layout>
)

export const query = graphql`
  query {
    file(relativePath: { eq: "self.jpg" }) {
      childImageSharp {
        fluid {
            ...GatsbyImageSharpFluid
        }
      }
    }
  }
`
