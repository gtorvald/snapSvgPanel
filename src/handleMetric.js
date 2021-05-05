export const handleMetricCode =
`var s = Snap(svgnode);
var rect = s.selectAll("rect");
for (let i = 0; i < rect.length; i++)
{
    var data = ctrl.getSeriesElementByAlias(rect[i].node.id)
    if (data !== null) {
        let val = data.datapoints[0][0];
        if (val < 50)
            rect[i].attr({
                fill: '#489542ff' // green
            });
        else if (val < 75)
            rect[i].attr({
                fill: '#c6c71aff' // yellow
            });
        else
            rect[i].attr({
                fill: '#b83232ff' //red
            });
    }
}`