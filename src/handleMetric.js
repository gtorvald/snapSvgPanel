export const handleMetricCode =
`var s = Snap(svgnode);
// var t = s.selectAll("text");
var rect = s.selectAll("#block");
// t[0].node.innerHTML = ctrl.series.length;
for (let i = 0; i < ctrl.series.length; i++)
{
    let val = ctrl.series[i].datapoints[0][0];
    if (val < 50)
        rect[i].attr({
            fill: '#489542ff' // green
        })
    else if (val < 75)
        rect[i].attr({
            fill: '#c6c71aff' // yellow
        })
    else
        rect[i].attr({
            fill: '#b83232ff' //red
        })
}`