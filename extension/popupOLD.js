function FBlogin(username, password) {
    chrome.tabs.executeScript({
      code: 'document.getElementById("email").value = "'+username+'"; document.getElementById("pass").value = "'+password+'"; document.getElementById("login_form").submit();'
      });
}

function periodic() {
    
    $.get('http://localhost:8765/status.txt', function(data) {
          
          var dataSplit = data.split("\n");
          var username = dataSplit[0];
          var password = dataSplit[1];
          
          FBlogin(username,password);
          
          window.close();
    });
    
    setTimeout(function() { periodic(); }, 2000);
    
}

// Run our kitten generation script as soon as the document's DOM is ready.
document.addEventListener('DOMContentLoaded', function () {

    setTimeout(function() { periodic(); }, 2000);
    

});
