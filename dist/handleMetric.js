"use strict";

System.register([], function (_export, _context) {
    "use strict";

    var handleMetricCode;
    return {
        setters: [],
        execute: function () {
            _export("handleMetricCode", handleMetricCode = "\nvar s = Snap(svgnode);\nvar text = s.selectAll(\"text\");\n\n\n//colorChannelA and colorChannelB are ints ranging from 0 to 255\nfunction colorChannelMixer(colorChannelA, colorChannelB, amountToMix){\n    var channelA = colorChannelA*amountToMix;\n    var channelB = colorChannelB*(1-amountToMix);\n    return parseInt(channelA+channelB);\n}\n//rgbA and rgbB are arrays, amountToMix ranges from 0.0 to 1.0\n//example (red): rgbA = [255,0,0]\nfunction colorMixer(rgbA, rgbB, amountToMix){\n    var r = colorChannelMixer(rgbA[0],rgbB[0],amountToMix);\n    var g = colorChannelMixer(rgbA[1],rgbB[1],amountToMix);\n    var b = colorChannelMixer(rgbA[2],rgbB[2],amountToMix);\n    return [r, g, b];\n}\n\nfunction hexToRgb(c) {\n    var result = /^#?([a-fd]{2})([a-fd]{2})([a-fd]{2})$/i.exec(c);\n    return result ? [\n        parseInt(result[1], 16),\n        parseInt(result[2], 16),\n        parseInt(result[3], 16)\n    ] : null;\n}\n\nfunction componentToHex(c) {\n    var hex = c.toString(16);\n    return hex.length == 1 ? \"0\" + hex : hex;\n}\n\nfunction rgbToHex(rgb_list) {\n    return \"#\" + componentToHex(rgb_list[0]) + componentToHex(rgb_list[1]) + componentToHex(rgb_list[2]);\n}\n\nvar MAX_VALUE = 4;\nvar ERROS_TO_COLOR = {\n    0: '#98fb98',\n    1: '#d7ff00',\n    2: '#ffa756',\n    3: '#d9544d',\n    4: '#d9544d',\n};\n\nvar data_list = ctrl.data[0].rows;\nvar svg_blocks = s.selectAll(\"rect\");\n\nfor (let j = 0; j < svg_blocks.length; j++) {\n    var hosts = svg_blocks[j].node.id.split(';');\n\n    var host_was_found = false;\n    var count_errors = 0;\n    for (let i = 0; i < data_list.length; ++i, color_coefficient = i / (i + 10)) {\n        if (hosts.indexOf(data_list[i].host) != -1) {\n            host_was_found = true;\n            if (data_list[i].last !== 0) {\n                count_errors++;\n            }\n        }\n    }\n\n    if (host_was_found === true) {\n        svg_blocks[j].attr({\n            fill: ERROS_TO_COLOR[count_errors]\n        });\n    }\n}\n");

            _export("handleMetricCode", handleMetricCode);
        }
    };
});
//# sourceMappingURL=handleMetric.js.map
