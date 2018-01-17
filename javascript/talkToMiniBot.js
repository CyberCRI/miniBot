function talkToMiniBot() {
  var userInput = document.forms["userInput"]["userInput"].value;
  if (userInput == "") {
    alert("Please say something.");
    return false;
  }
}
