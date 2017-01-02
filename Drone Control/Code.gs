function doGet(e) {
  
  if (e.parameter.control != undefined){
   return HtmlService.createTemplateFromFile("Page").evaluate().setTitle("Drone Control to Major Tom");
  }
  
  return ContentService.createTextOutput(getActions());
  
}

function getActions (){

  var docName = "EESDroneAction"; //We have a doc called EESDroneAction to store the data. It's lazy ik but bare easy.
  var file, files = DriveApp.getFilesByName(docName); //Retrieve the ID
  
  //Check if the doc exists. If it doesn't, return nothing
  if (files.hasNext ()){
   file = files.next(); 
  } else {
    return "";
  }
  
  var docId = file.getId();
  var doc = DocumentApp.openById(docId); //Get the doc
  var text = doc.getBody().editAsText().getText(); //Retrieve text as a string

  return text.trim();
  
}

function doActions (actions){ //Assume that actions are in a string "action1 action2 action3..."

  var docName = "EESDroneAction";
  var file, files = DriveApp.getFilesByName(docName); 
  
  //Check if the doc exists. If it doesn't, return error
  if (files.hasNext ()){
   file = files.next(); 
  } else {
    return "Error";
  }
  
  var docId = file.getId();
  var doc = DocumentApp.openById(docId); //Get the doc
  var text = doc.getBody().editAsText().getText(); //Retrieve text as a string

  doc.setText('');
  doc.getBody().appendParagraph (actions);

  
}


