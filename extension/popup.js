
var gotGesture = false;

//method invoked by the python code
var js_sum = function(a, b) {
    return a + b;
}

// Make sure slurpy loaded properly
 python.on('ready', function(evt) {
                python.dirname('/etc/passwd', function(response) {
                    console.log("Directory name" + response);
                });

                python.os.getenv("HOME", function(response) {
                    console.log("Home variable " + response);
                });

            
                python.os.getuid(function(uid) {
                    console.log("Current UID " + uid);
                });

                python.getGesture(function(response) {
                    console.log("Gesture ID" + response);
                });
});




function loginToFacebook(username, password) {
    chrome.tabs.executeScript({
      code: 'document.getElementById("email").value = "'+username+'"; document.getElementById("pass").value = "'+password+'"; document.getElementById("login_form").submit();'
      });
}

document.addEventListener('DOMContentLoaded', function () {
    
    /* Show welcome, username selection screen */
    
    /* When user clicks a user profile, proceed with reading handshake */
    $(".profile-img").click(function(event) {
       
        var email = event.target.title;
       
        $("#profile-selection-box").css("display","none");
        $("#handshake-progress-box").css("display","block");

        /* read the handshake */
        var gestures = new Array();
        for (var i = 0; i < 3; i++){
           
            $(".signal").css("display","none");    
            $("#signal"+i).css("display","block");
            console.log("#signal"+i);
            
            python.getGesture(-1, function(response){console.log("Gesture ID " + response); window.gestures[i] = response; window.gotGesture = true;});
                            
            while (window.gotGesture == false) {
                var blah = true;
            }
            
            window.gotGesture = false;

        }

        $(".signal").css("display","none");    
        $("#signal3").css("display","block");
                            
        console.log(gestures);

    });

    

});
