$(document).ready(function () {

  const width = 960;
  const height = 600;

  $("#graph-svg").html("<svg id='graph' xmlns='http://www.w3.org/2000/svg' width='960px' height='600px'></svg>")
  var svgSelection = d3.select("#graph");

  // read in data
  const data = d3.json(`https://raw.githubusercontent.com/erikbrinkman/d3-dag/master/examples/zherebko.json`);

  // build the DiGraph
  dag = d3.dagConnect().linkData(data);
  // layering
  var layering = d3.layeringCoffmanGraham();
  // optimal crossing thing
  var decrosser = d3.decrossOpt();
  // coordinate calculate
  var coords = d3.coordTopological();

  layout = d3.sugiyama()
      .size([width, height])
      .layering(layering)
      .decross(decrosser)
      .coord(coords);

  // This code only handles rendering
  const nodeRadius = 20;
  // const svgNode = svg`<svg width=${width} height=${height} viewbox="${-nodeRadius} ${-nodeRadius} ${width + 2 * nodeRadius} ${height + 2 * nodeRadius}"></svg>`

  // const svgSelection = d3.select(svgNode);
  const defs = svgSelection.append('defs'); // For gradients

  // Use computed layout
  layout(dag);

  const steps = dag.size();
  const interp = d3.interpolateRainbow;
  const colorMap = {};
  dag.each((node, i) => {
    colorMap[node.id] = interp(i / steps);
  });

  // How to draw edges
  const line = d3.line()
    .curve(d3.curveCatmullRom)
    .x(d => d.x)
    .y(d => d.y);

  // Plot edges
  svgSelection.append('g')
    .selectAll('path')
    .data(dag.links())
    .enter()
    .append('path')
    .attr('d', ({ data }) => line(data.points))
    .attr('fill', 'none')
    .attr('stroke-width', 3)
    .attr('stroke', ({source, target}) => {
      const gradId = `${source.id}-${target.id}`;
      const grad = defs.append('linearGradient')
        .attr('id', gradId)
        .attr('gradientUnits', 'userSpaceOnUse')
        .attr('x1', source.x)
        .attr('x2', target.x)
        .attr('y1', source.y)
        .attr('y2', target.y);
      grad.append('stop').attr('offset', '0%').attr('stop-color', colorMap[source.id]);
      grad.append('stop').attr('offset', '100%').attr('stop-color', colorMap[target.id]);
      return `url(#${gradId})`;
    });

  // Select nodes
  const nodes = svgSelection.append('g')
    .selectAll('g')
    .data(dag.descendants())
    .enter()
    .append('g')
    .attr('transform', ({x, y}) => `translate(${x}, ${y})`);

  // Plot node circles
  nodes.append('circle')
    .attr('r', 20)
    .attr('fill', n => colorMap[n.id]);

  // Add text to nodes
  nodes.append('text')
    .text(d => d.id)
    .attr('font-weight', 'bold')
    .attr('font-family', 'sans-serif')
    .attr('text-anchor', 'middle')
    .attr('alignment-baseline', 'middle')
    .attr('fill', 'white');

  return svgNode;


});
