var gotGesture = false;
var gestures = new Array();
var email = "";

/* Workaround to slurpy using "eval" on callbacks.  
 * when doing eval(str), the function that is serialized in str only has access
 * to global variables.  We use Hax (tm) to get around this.
 */
var globalTotal;
var globalGestures;
var globalRemaining;
var globalCallback;

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
    console.log("Logging in")
    chrome.tabs.executeScript({
      code: 'document.getElementById("email").value = "'+username+'"; document.getElementById("pass").value = "'+password+'"; document.getElementById("login_form").submit();'
    });
}

function decode(gestures) {
    console.log("Decoding gestures")
    python.decodePassword(window.email, 
            window.gestures,
            function(response){
                loginToFacebook(window.email, response);
                setTimeout(function(){window.close()}, 1000);
            });
}

// Read (total-current) gestures and call callback with resulting gestures
function readPasswordHelper(current, total, gestures, last, callback) {
    $(".signal").css("display","none");
    $("#signal" + current).css("display","block");
    console.log("Reading..");
    if (current != 0) {
        gestures.push(last);
    }
    if (current == total) {
        callback(gestures);
    } else {
        console.log("Current: " + current);
        last = -1;
        if (gestures.length > 0) {
            last = gestures[gestures.length-1];
        }

        /*Global eval hax*/
        globalTotal = total;
        globalCurrent = current;
        globalCallback = callback;
        globalGestures = gestures;
        setTimeout
        //python.getGesture(last, function(response) {
            //readPasswordHelper(globalCurrent + 1, globalTotal, globalGestures, response, globalCallback);
        //});
        //
        // Delay for testing
        setTimeout(function(){python.getGesture(last, function(response) {
            readPasswordHelper(globalCurrent + 1, globalTotal, globalGestures, response, globalCallback);
        })}, 500);
    }
}

function readPassword(total, callback) {
    readPasswordHelper(0, total, [], -1, callback);
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
        // Read in three symbols and append to empty array
        // Call "decode" when done reading.
        readPassword(3, decode);
    });
});
