$(document).ready(function(){
    // This loads the Google Charts and calls the functions that draw them
    google.charts.load('current', {'packages':['corechart']});
    google.charts.setOnLoadCallback(drawChart);
    console.log('hey');

    // Event occurs when users clicks on button to start auto test
    $("#autoTestBtn").on('click', function(){

    });

    $("#manualTestBtn").on('click', function(){
        alert("placeholder")
    })
});

function drawChart() {
    // This array hold the data that is placed in the charts
    var supplyData = google.visualization.arrayToDataTable([
      ['Time', 'Recorded Pressure', 'Limit'],
      [0,  1000, 1200],
      [2,  1170, 1200],
      [3,  660, 1200],
      [4,  1030, 1200],
      [5,  700, 1200],
      [6,  930, 1200],
      [7,  500, 1200],
      [8,  670, 1200],
      [9,  583, 1200],
      [10,  1000, 1200],
    ]);

    var controlData = google.visualization.arrayToDataTable([
        ['Time', 'Recorded Pressure', 'Limit', 'Limit2'],
        [0,  1000, 1200, 1350],
        [2,  1170, 1200, 1350],
        [3,  660, 1200, 1350],
        [4,  1030, 1200, 1350],
        [5,  700, 1200, 1350],
        [6,  930, 1200, 1350],
        [7,  500, 1200, 1350],
        [8,  670, 1200, 1350],
        [9,  583, 1200, 1350],
        [10,  1000, 1200, 1350],
      ]);

    var document_width = $(document).width();

    var options = {
      title: 'Supply Pressure',
      width: document_width / 2.2,
      vAxis: { title: 'Pressure (psi)', gridlines: { count: 10 }, minValue: 0, maxValue: 1300},
      hAxis: { title: 'Time (seconds)', gridlines: { count: 10 }, minValue: 0},
      series: {1: {type: 'line'}},
      legend: { position: 'bottom' }
    };

    var supplyChart = new google.visualization.ComboChart($(".supply_chart")[0]);
    var controlChart = new google.visualization.LineChart($(".control_chart")[0]);

    supplyChart.draw(supplyData, options);

    // Change the chart options before drawing the control chart
    options.title = 'Control Pressure';

    controlChart.draw(controlData, options);
  }