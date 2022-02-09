

var endpoint= '/api/data/sensor{{i}}'
var chartHistorialHumedadData=[]
var chartHistorialHumedadLabels=[]

$.ajax({
method: "GET",
url: endpoint,
success: function(data){
    chartHistorialHumedadData = data.default
    chartHistorialHumedadLabels = data.labels
    var ctx = document.getElementById('chart-historial-humedad-{{i}}').getContext('2d')
    var myChart = new Chart(ctx, {
    type: 'line',
    data: {
    labels: chartHistorialHumedadLabels,
    datasets: [{
        label: 'Historial Humedad del Suelo Promedio',
        data: chartHistorialHumedadData,
    }]
    },
    }) 
},
error: function(error_data){
    console.log("error")
    console.log(error_data)
}

})  

