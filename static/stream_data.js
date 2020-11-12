function getWindow(lastDate) {
    var window = $('meta[name=x_window]').attr("content");
    var lastDateObj = new Date(lastDate);
    var windowDateObj = lastDateObj.setSeconds(lastDateObj.getSeconds() - window);
    return windowDateObj;
}

function makePlotly( x, y ){
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
                  showlegend: true,
                    legend: {
                            x: .99,
                            y: .98,
                            bgcolor: '#fff',
                            xanchor: 'right',
                            yanchor: 'top',
                            traceorder: 'normal',
                            bordercolor: '#000',
                            borderwidth: 2
                  },
                  yaxis: {
                        linecolor: 'black',
                        linewidth: 2,
                        mirror: true,
                        automargin: true,
                      // gridcolor: '#000',
                      // gridwidth: 'rgb(255, 255, 2555)',
                        range: [0, 100],
                        title: "Random Number",
                        dtick: 5
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

function streamPlotly( x, y ){
    var plotDiv = document.getElementById("plot");
    var data_update = {x: [x], y: [y]}
    var windowDateObj = getWindow(x)
    var layout_update = {xaxis: {
        range: [windowDateObj, x[x.length - 1]],
        rangeslider: {range: [plot_start, x[x.length - 1]]}
    }};
    Plotly.update(plotDiv, {}, layout_update)
    Plotly.extendTraces(plotDiv, data_update, [0])
};

var url = 'http://' + document.domain + ':' + location.port
var socket = io.connect(url);

socket.on('connect', function(msg) {
    console.log('connected to websocket on ' + url);
});

socket.on('bootstrap', function (msg) {
    plot_start = msg.x[0];
    makePlotly( msg.x, msg.y )
    console.log(msg.x, msg.y)
});

socket.on('update', function (msg) {
    console.log(msg.x, msg.y );
    streamPlotly( msg.x, msg.y )
});

socket.on('reply-message', function (msg) {
    if (msg === 'opened'){
        $("#solenoid-one").checked = true;
    }
    if (msg === 'closed'){
        $("#solenoid-one").checked = false;
    }
});

$(document).ready(function(){
    $("#solenoid-one").click(function(){
        if($(this).prop("checked") == true){
            console.log("Checkbox is checked.");
            socket.emit("message", "on_0")
        }
        else if($(this).prop("checked") == false){
            console.log("Checkbox is unchecked.");
            socket.emit("message", "off_0")
        }
    });
});
