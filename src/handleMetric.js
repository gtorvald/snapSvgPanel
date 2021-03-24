export const handleMetricCode =
`var s = Snap(svgnode);
// var t = s.selectAll("text");
var rect = s.selectAll("rect");
// t[0].node.innerHTML = ctrl.series.length;
for (let i = 0; i < ctrl.series.length; i++)
{
    let val = ctrl.series[i].datapoints[0][0];
    if (val < 50)
        rect[i + 1].attr({
            fill: 'green'
        })
    else if (val < 75)
        rect[i + 1].attr({
            fill: 'yellow'
        })
    else
        rect[i + 1].attr({
            fill: 'red'
        })
}`
// t[0].node.innerHTML = ctrl.series[0].datapoints[0][0];