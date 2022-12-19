
        $(document).ready(function () {

          //create baselayer
          var baseLayer = L.tileLayer(
        'http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',{
          attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
          maxZoom: 20
          });


      // features of heatlayer
      var cfg = {
    
        "radius":60,
        "maxOpacity":1,
        "scaleRadius": false,
        "useLocalExtrema": true,
        latField: 'lat',
        lngField: 'lng',
        valueField: 'score',
        gradient: {
        0.0: 'blue',
        0.3: 'cyan',
        0.6: 'green',
        0.6: 'yellow',
        0.7: 'violet',
        0.8: 'white',
        0.9: 'pink',
        1.0: 'red'},
      };
     
      //create heatlayer using heatmapoverlay lib
      var heatmapLayer = new HeatmapOverlay(cfg);
    
      //create map
      var map = new L.Map('map', {
       center: new L.LatLng(20.000,-50.000),
       zoom: 2,
       layers: [baseLayer, heatmapLayer]
     });
    
    
     
     $("form").submit(function (event) {
  
      event.preventDefault();

      //list to contain returned data from query srvice
      let mapData = []
            
          
     // to make result logic and to prevernt server errors
                
     if($("#llon").val() > $("#rlon").val()){
      alert("right longitude should be greater then left longitude");
     }
     if($("#blat").val() >  $("#tlat").val()){
      alert("top latitude should be greater then buttom longitude");
     }
     else{

      // here all process eill be implemented

      //data from html form
      var formData = {
        text: $("#text").val(),
        llon: $("#llon").val(), // left longitude
        rlon: $("#rlon").val(), // right longitude
        tlat: $("#tlat").val(), // top latitude
        blat: $("#blat").val(), // buttom latitude
        gte: $("#gte").val(),   // start date of range
        lte: $("#lte").val(),   // end date of range

      };

      // print form data to console
      console.log(formData);
 
      // request to query service to get tweets data
      // from elasticserch then plot it using heatmap 
      $.ajax({
      
        type: "GET",
        dataType: "json",
        jsonp: false,
        jsonpCallback: false,
        contentType: "application/javascript",
        data: formData,
        async: false,
        url: "/get",

    success: function (jsonData) {
      //print returned data
      console.log(jsonData);
      

  // if there is no data returned
   if (Object.keys(jsonData).length === 0){
   alert("there is no tweets according to your inputs")
   }

   
   // push returned data to mapData list 
   // on shape [{'lat' : val, 'lng' : val, 'score' : val}, {.....}]
   Object.keys(jsonData).forEach(function(key) {
        console.log(key, jsonData[key]);
        mapData.push(jsonData[key])
});
   
},

// print error when happen
error: function (request, textStatus, errorThrown) {
   console.log(request.responseText);
   console.log(textStatus);
   console.log(errorThrown);
}
});


//data to set in heatlayer
var testData = {
data: mapData
};

// set data to heatlayer
heatmapLayer.setData(testData);

     }

     })});
  