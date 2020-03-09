const path = require(`path`)

exports.createPages = async ({actions, graphql, reporter }) => {
    const { createPage } = actions
    const projectTemplate = path.resolve(`src/templates/project.js`)
    const result = await graphql(`
        {
            allMarkdownRemark(
                sort: { order: DESC, fields: [frontmatter___date]}
                limit: 1000
            ) {
                edges {
                    node {
                        frontmatter {
                            path
                        }
                    }
                }
            }
        }
    `)

    if (result.errors) {
        reporter.panicOnBuild(`Error while running GraphQL query.`)
        return
    }

    result.data.allMarkdownRemark.edges.forEach(({ node }) => {
        createPage({
            path: node.frontmatter.path,
            component: projectTemplate,
            context: {},
        })
    }) 
}
// exports.onCreateWebpackConfig = ({stage, loaders, actions }) => {
  // if(state == `build-html`) {
    // actions.setWebpackConfig({
      // module: {
        // rules: [
          // {
            // rest: /plotly/,
            // use: loaders.null(),
          // },
        // ],
      // },
    // });
  // }
// }
