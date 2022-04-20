export const handleMetricCode =
`
var s = Snap(svgnode);
var text = s.selectAll("text");


//colorChannelA and colorChannelB are ints ranging from 0 to 255
function colorChannelMixer(colorChannelA, colorChannelB, amountToMix){
    var channelA = colorChannelA*amountToMix;
    var channelB = colorChannelB*(1-amountToMix);
    return parseInt(channelA+channelB);
}
//rgbA and rgbB are arrays, amountToMix ranges from 0.0 to 1.0
//example (red): rgbA = [255,0,0]
function colorMixer(rgbA, rgbB, amountToMix){
    var r = colorChannelMixer(rgbA[0],rgbB[0],amountToMix);
    var g = colorChannelMixer(rgbA[1],rgbB[1],amountToMix);
    var b = colorChannelMixer(rgbA[2],rgbB[2],amountToMix);
    return [r, g, b];
}

function hexToRgb(c) {
    var result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(c);
    return result ? [
        parseInt(result[1], 16),
        parseInt(result[2], 16),
        parseInt(result[3], 16)
    ] : null;
}

function componentToHex(c) {
    var hex = c.toString(16);
    return hex.length == 1 ? "0" + hex : hex;
}

function rgbToHex(rgb_list) {
    return "#" + componentToHex(rgb_list[0]) + componentToHex(rgb_list[1]) + componentToHex(rgb_list[2]);
}

var MAX_VALUE = 4;
var ERROS_TO_COLOR = {
    0: '#98fb98',
    1: '#d7ff00',
    2: '#ffa756',
    3: '#d9544d',
    4: '#d9544d',
};

var data_list = ctrl.data[0].rows;
var svg_blocks = s.selectAll("rect");

for (let j = 0; j < svg_blocks.length; j++) {
    var hosts = svg_blocks[j].node.id.split(';');

    var host_was_found = false;
    var count_errors = 0;
    for (let i = 0; i < data_list.length; ++i, color_coefficient = i / (i + 10)) {
        if (hosts.indexOf(data_list[i].host) != -1) {
            host_was_found = true;
            if (data_list[i].last !== 0) {
                count_errors++;
            }
        }
    }

    if (host_was_found === true) {
        svg_blocks[j].attr({
            fill: ERROS_TO_COLOR[count_errors]
        });
    }
}
`
