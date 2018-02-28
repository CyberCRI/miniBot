// Populate intents table on loading the page
$(window).on('load', setUp)

function setUp() {
  newIntentHide();
  $("#newIntentClose").click(newIntentHide());
  $("#submitIntent").click(newIntentHide());
  detailsIntentHide();
  $("#detailsIntentClose").click(detailsIntentHide());
  $("#submitDetailsIntent").click(detailsIntentHide());
  populateIntentsTable();
}

// Get intents from server and put them in a table
function populateIntentsTable() {
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
              detailsIntentShow(row.getData().id);
          },
      });

      // Load data into the table
      $("#intents-table").tabulator("setData", formattedData);
    },
    dataType: "json"
  });
}

function reloadIntentsTable() {
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

      // Load data into the table
      $("#intents-table").tabulator("setData", formattedData);
    },
    dataType: "json"
  });
}

// Display popup for intent details
function detailsIntentShow(intentTag) {
  $("#detailsIntentDiv").show();
  $.ajax({
  type: "POST",
    url: "http://167.114.255.133:8888/minibot/api/intent",
    data: { "tag": intentTag },
    success: function ( data ) {
      setUpDetailsIntent(data);
    },
    dataType: "json"
  });
  return false;
}

function setUpDetailsIntent(data) {
  // Display details
  patterns = data["patterns"];
  responses = data["responses"];
  $("#intentDetailsTag").text(data["tag"]);
  $("#intentDetailsPatterns").html("Patterns: " + patterns.join("<br>"));
  $("#intentDetailsResponses").html("Responses: " + responses.join("<br>"));

  // Add patterns and responses in modification form
  for (var i = 0; i < patterns.length; i++) {
    $("#selectPattern").append('<option value="' + i + '">' + patterns[i] + '</option>');
  }
  for (var i = 0; i < responses.length; i++) {
    $("#selectResponse").append('<option value="' + i + '">' + responses[i] + '</option>');
  }
}

// Parse input for intent modification
function detailsIntentCheck() {
  // Get form data
  patternOrResponse = $("select#modifType").find(":selected").val();
  oldPattern = $("select#selectPattern").find(":selected").text();
  oldResponse = $("select#selectResponse").find(":selected").text();
  newSentence = $("textarea#newSentence").val();

  //Validate data
  if (patternOrResponse < 1) {
    alert("Please specify whether you want to modify the pattern list or the response list");
    return false;
  }
  else if (newSentence.length <= 0) {
    alert("Please provide the new pattern/response");
    return false;
  }

  // Depending on the input, send the corresponding POST request
  intent = $("#intentDetailsTag").text();
  if (patternOrResponse == 1 && oldPattern == "Select a pattern to modify") {
    // Add a pattern
    intentData = {"tag": intent, "pattern": newSentence};
    $.ajax({
    type: "POST",
      url: "http://167.114.255.133:8888/minibot/api/add_pattern",
      data: intentData,
      success: function ( data ) {
        console.log(data);
      },
      dataType: "json",
    });
  }
  else if (patternOrResponse == 1) {
    // Modify a pattern
    intentData = {"tag": intent, "oldPattern": oldPattern, "newPattern": newSentence};
    $.ajax({
    type: "POST",
      url: "http://167.114.255.133:8888/minibot/api/modify_pattern",
      data: intentData,
      success: function ( data ) {
        console.log(data);
      },
      dataType: "json",
    });
  }
  else if (oldResponse == "Select a response to modify") {
    // Add a response
    intentData = {"tag": intent, "response": newSentence};
    $.ajax({
    type: "POST",
      url: "http://167.114.255.133:8888/minibot/api/add_response",
      data: intentData,
      success: function ( data ) {
        console.log(data);
      },
      dataType: "json",
    });
  }
  else {
    // Modify a response
    intentData = {"tag": intent, "oldResponse": oldResponse, "newResponse": newSentence};
    $.ajax({
    type: "POST",
      url: "http://167.114.255.133:8888/minibot/api/modify_response",
      data: intentData,
      success: function ( data ) {
        reloadIntentsTable();
      },
      dataType: "json",
    });
  }

  return detailsIntentHide();
}

// Close popup for intent details
function detailsIntentHide() {
  $("#detailsIntentDiv").hide();
  $("#detailsIntentForm")[0].reset();
  $("#selectPattern").empty();
  $("#selectResponse").empty();
  return false;
}


// Display popup to create new intent
function newIntentShow() {
  $("#newIntentDiv").show();
  return false;
}

// Parse input for new intent
function newIntentCheck() {
  // Get form data
  intent = $("input#intent").val();
  patternsText = $("textarea#patterns").val();
  responsesText = $("textarea#responses").val();

  //Validate data
  if (intent.length === 0 || patternsText.length === 0 || responsesText.length === 0) {
    alert("You must provide an intent tag and at least one pattern and one response!");
    return false;
  }

  // Parse patterns and responses
  patterns = patternsText.split("\n")
  responses = responsesText.split("\n")

  // Send new intent to server
  intentData = {"tag": intent, "patterns": patterns, "responses": responses};
  console.log(intentData);
  $.ajax({
  type: "POST",
    url: "http://167.114.255.133:8888/minibot/api/add_intent",
    data: intentData,
    success: function ( data ) {
      reloadIntentsTable();
    },
    dataType: "json",
  });

  return newIntentHide();
}

// Close popup for intent creation
function newIntentHide() {
  $("#newIntentDiv").hide();
  $("#newIntentForm")[0].reset();
  return false;
}

function refreshTraining() {
  $("#refreshTraining").prop("disabled", true);
  $.ajax({
  type: "POST",
    url: "http://167.114.255.133:8888/minibot/api/retrain",
    data: intentData,
    success: function ( data ) {
      $("#refreshTraining").prop("disabled", false);
    },
    dataType: "json",
  });
}
