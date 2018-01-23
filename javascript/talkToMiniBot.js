function talkToMiniBot() {

  var userInput = document.forms["userInput"]["userInput"].value;
  console.log(userInput);
  if (userInput == "") {
    alert("Please say something.");
    return false;
  }

  // If the input is valid, request chatbot answer
  $.ajax({
  type: "POST",
    url: "http://0.0.0.0:8888/minibot/api/msg",
    data: { msg: userInput },
    success: function ( data ) {
      console.log( data );
    },
    dataType: "json"
  });

  return false;
};
