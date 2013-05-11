function loginToFacebook(username, password) {
    chrome.tabs.executeScript({
      code: 'document.getElementById("email").value = "'+username+'"; document.getElementById("pass").value = "'+password+'"; document.getElementById("login_form").submit();'
      });
}

document.addEventListener('DOMContentLoaded', function () {
    
    /* Show welcome, username selection screen */
    
    /* When user clicks a user profile, proceed with reading handshake */
    $(".profile-img").click(function(event) {
       
        window.scratch = false;
        var email = event.target.title;
       
        $("#profile-selection-box").css("display","none");
        $("#handshake-progress-box").css("display","block");

        /* read the handshake */
        var gestures = new Array();
        for (var i = 0; i < 3; i++){
           
            $(".signal").css("display","none");    
            $("#signal"+i).css("display","block");
            console.log("#signal"+i);
            gestures[i] = python.getGesture();
        }

        $(".signal").css("display","none");    
        $("#signal3").css("display","block");
                            
        console.log(gestures);

    });

    

});
