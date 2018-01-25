function talkToMiniBot() {

  var userInput = document.forms["userInput"]["userInput"].value;
  if (userInput == "") {
    alert("Please say something.");
    return false;
  }

  // If the input is valid, update history and request chatbot answer
  var previousBotMsg = $("#botDiv").html();
  var userMsgHTML = "<p>" + userInput + "</p>";
  $("#historyDiv").append("<p><b>Bot:</b></p>", previousBotMsg, "<p><b>You:</b></p>", userMsgHTML);
  document.forms["userInput"]["userInput"].value = "";

  // HTTP POST request for chatbot answer
  $.ajax({
  type: "POST",
    url: "http://0.0.0.0:8888/minibot/api/msg",
    data: { msg: userInput },
    success: function ( data ) {
      botMsg = data["msg"];
      formattedMsg = "<p>" + botMsg + "</p>";
      $("#botDiv").html(formattedMsg);
    },
    dataType: "json"
  });

  return false;
};
