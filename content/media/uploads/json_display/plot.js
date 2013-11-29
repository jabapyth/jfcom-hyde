
if (typeof(title) == "undefined") title = 'JSON parsing in Python';

var chart = new Highcharts.Chart({
   chart: {
      renderTo: 'plot',
      margin: [50, 80, 100, 50],
      zoomType: 'xy'
   },
   title: {
      text: title,
      style: {
         margin: '10px 0 0 0' // center it
      }
   },
   xAxis: [{
      categories: titles,
      labels: {
         rotation: -45,
         align: 'right',
         x: 10,
         y: 10
      },
      minPadding: 50
   }],
   yAxis: [{ // Primary yAxis
      labels: {
         style: {
            color: '#89A54E'
         },
      },
      title: {
         text: 'Lines of Code',
         style: {
            color: '#89A54E'
         },
         margin: 50
      },
      opposite: true
      
   }, { // Secondary yAxis
      title: {
         text: 'Execution time',
         margin: 40,
         style: {
            color: '#4572A7'
         }
      },
      labels: {
         formatter: function() {
            return this.value +'s';
         },
         style: {
            color: '#4572A7'
         }
      }
      
   }],
   tooltip: {
      formatter: function() {
         var unit = {
            'Size': 'lines',
            'Execution time': 'seconds',
         }[this.series.name];
         
         return '<b>'+ this.series.name +'</b><br/>'+
            this.x +': '+ ('' + this.y).slice(0,5) +' '+ unit;
      }
   },
   legend: {
      layout: 'vertical',
      style: {
         left: '120px',
         bottom: 'auto',
         right: 'auto',
         top: '90px'
      },
      backgroundColor: '#FFFFFF'
   },
   series: [{
      name: 'Execution time',
      color: '#4572A7',
      type: 'column',
      yAxis: 1,
      data: results
   
   }, {
      name: 'Size',
      color: '#89A54E',
      type: 'column',
      yAxis: 0,
      data: lines
   }]
});



