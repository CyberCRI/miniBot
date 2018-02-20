
$(window).on('load', populateIntentsTable())

function populateIntentsTable() {
  // Get intents from server and put them in a table
  $.ajax({
  type: "POST",
    url: "http://167.114.255.133:8888/minibot/api/intents",
    data: { },
    success: function ( data ) {
      // Format data for the table
      formattedData = []
      for (var i = 0; i < data["intents"].length; i++) {
        intent = data["intents"][i];
        formattedIntent = {"id": intent["tag"], "tag": intent["tag"]};
        formattedIntent["pattern"] = intent["patterns"][0]; // Pick first pattern as an example
        formattedIntent["response"] = intent["responses"][0]; // Pick first response as an example
        formattedData.push(formattedIntent)
      }

      //create Tabulator on DOM element with id "intents-table"
      $("#intents-table").tabulator({
          height:205, // set height of table (in CSS or here), this enables the Virtual DOM and improves render speed dramatically (can be any valid css height value)
          layout:"fitColumns", //fit columns to width of table (optional)
          columns:[ //Define Table Columns
              {title:"Intent", field:"tag", width:100},
              {title:"Example pattern", field:"pattern", align:"left"},
              {title:"Example response", field:"response", align:"left"},
          ],
          rowClick:function(e, row){ //trigger an alert message when the row is clicked
              alert("Row " + row.getData().id + " Clicked!!!!");
          },
      });

      // Load data into the table
      $("#intents-table").tabulator("setData", formattedData);
    },
    dataType: "json"
  });
}
