import React from 'react';
import Plot from 'react-plotly.js';

const scatter = (args) => {
  return {
    x: JSON.parse(args.props.x),
    y: JSON.parse(args.props.y),
    mode: (args.props.mode !== undefined) ? args.props.mode : 'markers',
    name: (args.props.name !== undefined) ? args.props.name : undefined,
    type: 'scatter',
  };
}
const bar = (args) => {
  return {
    x: JSON.parse(args.props.x),
    y: JSON.parse(args.props.y),
    name: (args.props.name !== undefined) ? args.props.name : undefined,
    type: 'bar',
  };
}

const contour = (args) => {
  return {
    x: (args.props.x !== undefined) ? JSON.parse(args.props.x) : undefined,
    y: (args.props.y !== undefined) ? JSON.parse(args.props.y) : undefined,
    z: JSON.parse(args.props.z),
    name: (args.props.name !== undefined) ? args.props.name : undefined,
    ncontours: (args.props.ncontours !== undefined) ? args.props.ncontours : 32,
    showscale: (args.props.showscale !== undefined) ? args.props.showscale : false,
    colorscale: (args.props.colorscale !== undefined) ? args.props.colorscale : undefined,
    type: 'contour',
  };
}

const heatmap = (args) => {
  return {
    x: (args.props.x !== undefined) ? JSON.parse(args.props.x) : undefined,
    y: (args.props.y !== undefined) ? JSON.parse(args.props.y) : undefined,
    z: JSON.parse(args.props.z),
    name: (args.props.name !== undefined) ? args.props.name : undefined,
    showscale: (args.props.showscale !== undefined) ? args.props.showscale : false,
    colorscale: (args.props.colorscale !== undefined) ? args.props.colorscale : undefined,
    type: 'heatmap',
  };
}

export const Plotly = (args) => {
  let data = []
  for (const child of args.children) {
    if (typeof child === 'object') {
      if (child.type === "scatter") {
        data.push(scatter(child));
      } else if(child.type === "bar") {
        data.push(bar(child));
      } else if(child.type === "contour") {
        data.push(contour(child));
      } else if(child.type === "heatmap") {
        data.push(heatmap(child));
      }
    }
  }
  const layout = {
    title: args.title,
    margin: {t: 80, r: 64, b: 64, l: 64},
    autosize: true,
    xaxis: {
      title: {
        text: args.xaxis
      },
    },
    yaxis: {
      title: {
        text: args.yaxis
      },
    },
  };
  const config = {
    responsive: true
  };
  return (
    <div style={{margin: `15px`}}>
      <Plot layout={layout} style={{margin: `15px`, width: `100%`}} config={config} data={data} />
    </div>
  )
}

export const LazyPlot = (args) => {
  console.log(args);
  const data = {
    x: JSON.parse(args.x),
    y: JSON.parse(args.y),
    type: args.type,
    // type: JSON.parse(args.type),
  }
  console.log(data);
  return (<Plot data={[data]} layout={{margin: {t: 0, r: 0, l: 35}, autosize: true}} style={{width: `100%`}} autoResizeHandler/>)
}
