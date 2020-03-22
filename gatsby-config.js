module.exports = {
  siteMetadata: {
    title: `Arden Rasmussen`,
    siteUrl: `https://ardenrasmussen.com`,
    description: `Arden Rasmussen's personal website`,
  },
  plugins: [
    `gatsby-transformer-sharp`,
    `gatsby-plugin-sharp`,
    {
      resolve: `gatsby-source-filesystem`,
      options: {
        name: `projects`,
        path: `${__dirname}/pages/projects`,
      },
    },
    {
      resolve: `gatsby-source-filesystem`,
      options: {
        name: `images`,
        path: `${__dirname}/src/images`,
      },
    },
    {
      resolve: `gatsby-plugin-favicon`,
      options: {
        logo: "./src/favicon.png"
      }
    },
    {
      resolve: `gatsby-transformer-remark`,
      options: {
        plugins: [
          {
            resolve: `gatsby-remark-autolink-headers`,
            options: {}
          },
          { 
            resolve: `gatsby-remark-custom-blocks`,
            options: {
              blocks: {
                note: {
                  classes: "note",
                  title: "optional",
                },
                info: {
                  classes: "info",
                  title: "optional",
                },
                warn: {
                  classes: "warning",
                  title: "optional",
                },
                err: {
                  classes: "error",
                  title: "optional",
                }
              }
            }
          },
          {
            resolve: `gatsby-remark-katex`,
            options: {}
          },
          {
            resolve: `gatsby-remark-images`,
            options: {}
          },
          {
            resolve: `gatsby-remark-prismjs`,
            options: {}
          },
          {
            resolve: `gatsby-remark-copy-linked-files`,
            options: {
              destinationDir: f => `downloads/${f.hash}`,
              ignoreFileExtensions: [`png`, `jpg`, `jpeg`, `bmp`, `tift`]
            }
          }
        ]
      }
    }
  ]
}
