"use strict";

System.register([], function (_export, _context) {
    "use strict";

    var handleMetricCode;
    return {
        setters: [],
        execute: function () {
            _export("handleMetricCode", handleMetricCode = "var s = Snap(svgnode);\n// var t = s.selectAll(\"text\");\nvar rect = s.selectAll(\"rect\");\n// t[0].node.innerHTML = ctrl.series.length;\nfor (let i = 0; i < ctrl.series.length; i++)\n{\n    let val = ctrl.series[i].datapoints[0][0];\n    if (val < 50)\n        rect[i + 1].attr({\n            fill: 'green'\n        })\n    else if (val < 75)\n        rect[i + 1].attr({\n            fill: 'yellow'\n        })\n    else\n        rect[i + 1].attr({\n            fill: 'red'\n        })\n}");

            _export("handleMetricCode", handleMetricCode);
        }
    };
});
//# sourceMappingURL=handleMetric.js.map
