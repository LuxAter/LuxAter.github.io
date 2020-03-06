import React from "react"

import Layout from "../layouts/index"

import { Section } from "../components/typeogrophy"
import { Row, Column } from "../components/grid"

export default () => (
  <Layout>
    <Section id="aboutme">
      <h4>About Me</h4>
      <Row>
        <Column width="five">
          <em>Arden Rasmussen</em> is currently an Undergraduate student at
          Lewis and Clark College, majoring in Mathematics & Computer
          Science, with a sceond major in Physics.
        </Column>
        <Column width="five">
        </Column>
      </Row>
    </Section>
  </Layout>
)
