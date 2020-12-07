let downloadData = []
let recordData = false

function getWindow(lastDate) {
    var window = $('meta[name=x_window]').attr("content");
    var lastDateObj = new Date(lastDate);
    var windowDateObj = lastDateObj.setSeconds(lastDateObj.getSeconds() - window);
    return windowDateObj;
}

function makePlotly(x, y) {
    var plotDiv = document.getElementById("plot");
    var traces = [{
        type: 'scatter',
        x: x,
        y: y,
        line: {shape: 'spline', smoothing: 2, width: 3},
    }];
    const layout = {
        // paper_bgcolor: '#f4f1ef',
        plot_bgcolor: '#f4f1ef',
        autosize: true,
        title: "H<sub>2</sub> Sensor",
        showlegend: false,
        yaxis: {
            linecolor: 'black',
            linewidth: 2,
            mirror: true,
            automargin: true,
            // gridcolor: '#000',
            // gridwidth: 'rgb(255, 255, 2555)',
            autoscale: true,
            // range: [0, 100],
            title: "H<sub>2</sub> [ppm]",
            // dtick: 5
        },
        xaxis: {
            linecolor: 'black',
            linewidth: 2,
            mirror: true,
            automargin: true,
            rangeslider: {visible: true},
        },
        font: {
            size: 18
        }
    }
    const config = {
        responsive: true,
        'textSize': 22
    }
    Plotly.plot(plotDiv, traces, layout, config);
};

var plot_start = 0;

function streamPlotly(x, y) {
    var plotDiv = document.getElementById("plot");
    var data_update = {x: [x], y: [y]}
    var windowDateObj = getWindow(x)
    var layout_update = {
        xaxis: {
            range: [windowDateObj, x[x.length - 1]],
            rangeslider: {range: [plot_start, x[x.length - 1]]}
        }
    };
    Plotly.update(plotDiv, {}, layout_update)
    Plotly.extendTraces(plotDiv, data_update, [0])
};

var url = 'http://' + document.domain + ':' + location.port
var socket = io.connect(url);

socket.on('connect', function (msg) {
    console.log('connected to websocket on ' + url);
});

socket.on('bootstrap', function (msg) {
    plot_start = msg.x[0];
    makePlotly(msg.x, msg.y)
});

socket.on('update', function (msg) {
    streamPlotly(msg.x, msg.y);
    if (recordData === true) {
        downloadData.push({time: msg.x, value: msg.y})
    }
});

socket.on('reply-message', function (msg) {
    if (msg === 'in_valve_opened') {
        $("#solenoid-one").prop("checked", true)
    }
    if (msg === 'in_valve_closed') {
        $("#solenoid-one").prop("checked", false)
    }
    if (msg === 'out_valve_opened') {
        $("#solenoid-two").prop("checked", true)
    }
    if (msg === 'out_valve_closed') {
        $("#solenoid-two").prop("checked", false)
    }
});

function arrayToCSV(data) {
    csv = data.map(row => Object.values(row));
    csv.unshift(Object.keys(data[0]));
    return csv.join('\n');
}


$(document).ready(function () {
    let recording = false;

    function handleControl(url) {
        $.getJSON(url,
            function (data) {
                //do nothing
            });
    }

    $("#solenoid-one").click(function () {
        if ($(this).prop("checked") == true) {
            console.log("Checkbox is checked.");
            // socket.emit("message", "on_0")
            handleControl('/solenoid_1_on')
        } else if ($(this).prop("checked") == false) {
            console.log("Checkbox is unchecked.");
            // socket.emit("message", "off_0")
            handleControl('/solenoid_1_off')
        }
    });
    $("#solenoid-two").click(function () {
        if ($(this).prop("checked") == true) {
            console.log("Checkbox is checked.");
            // socket.emit("message", "on_1")
            handleControl('/solenoid_2_on')
        } else if ($(this).prop("checked") == false) {
            console.log("Checkbox is unchecked.");
            // socket.emit("message", "off_1");
            handleControl('/solenoid_2_off')
        }
    });
    $("#record-data").click(function () {
        recordData = true
        recording = true
        $(this).text('Recording...')
        $("#download-data").prop('disabled', false)
    });
    $("#download-data").click(function () {
        let filename = 'download.csv'
        if (recording === true) {
            recordData = false
            recording = false
            let csv = arrayToCSV(downloadData)
            var csvData = new Blob([csv], {type: 'text/csv;charset=utf-8;'});
            var csvURL = null;
            if (navigator.msSaveBlob) {
                csvURL = navigator.msSaveBlob(csvData, 'download.cv');
            } else {
                csvURL = window.URL.createObjectURL(csvData);
            }
            var tempLink = document.createElement('a');
            tempLink.href = csvURL;
            tempLink.setAttribute('download', 'download.csv');
            tempLink.click();
            downloadData = [];
            $("#record-data").prepend("<i class=\"fa fa-play\"></i>")
            $("#record-data").text('Record Data')
            $(this).prop('disabled', true)
        }
    });
});
