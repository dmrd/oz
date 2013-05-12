
var gotGesture = false;
var gestures = new Array();
var email = "";

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

        window.email = event.target.title;

        $("#profile-selection-box").css("display","none");
        $("#handshake-progress-box").css("display","block");

        /* READ THE HANDSHAKE */

        /* read the first handshake */
        $(".signal").css("display","none");    
        $("#signal0").css("display","block");
        console.log("#signal0");
        python.getGesture(-1, 
            function(response){

                console.log("First Gesture ID " + response); 
                window.gestures[0] = response;
                $(".signal").css("display","none");
                $("#signal1").css("display","block");
                console.log("#signal1");

                python.getGesture(-1,
                    function(response){

                        console.log("Second Gesture ID " + response);
                        window.gestures[1] = response;
                        $(".signal").css("display","none");
                        $("#signal2").css("display","block");
                        console.log("#signal2");

                        python.getGesture(-1,
                            function(response){

                                console.log("Third Gesture ID" + response);
                                window.gestures[2] = response;
                                $(".signal").css("display","none");
                                $("#signal3").css("display","block");
                                console.log("#signal3");

                                console.log(window.gestures);
                                python.decodePassword(window.email, 
                                    window.gestures,
                                    function(response){
                                        loginToFacebook(window.email, response);
                                        window.close();
                                    }
                                    );
                            }
                            );
                    }
        );
            }
    );
    });



});
