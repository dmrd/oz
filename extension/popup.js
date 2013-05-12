var gotGesture = false;
var gestures = new Array();
var email = "";
var fullname = "";
var password = "";

/* Workaround to slurpy using "eval" on callbacks.  
 * when doing eval(str), the function that is serialized in str only has access
 * to global variables.  We use Hax (tm) to get around this.
 */
var globalTotal;
var globalGestures;
var globalRemaining;
var globalCallback;

function loadProfiles(){
    python.listUsers(
        function(response){
            console.log(response);
            // response is a list of tuples
            for (var i = 0; i < response.length; i++) {
                var email = response[i][0];
                var fullname = response[i][1];
                $("#profile-selection-box").append('<div class="profile"><img class="profile-img" title="'+email+'" src="https://profile-b.xx.fbcdn.net/hprofile-prn1/161179_1452819135_1799331413_q.jpg"></img><br />'+fullname+'</div>');
            }
        });
}

function showScreen(divid){
    $(".centered-div").css("display","none");
    $("#"+divid).css("display","block");
}


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

function addUser(gestures) {
    console.log("Sending off user data to server")
    console.log(window.email)
    console.log(window.fullname)
    console.log(window.password)
    console.log(gestures)
    //Arguments need to be out of order... (gesture <-> password)
    python.addUser(window.email, 
            window.fullname,
            gestures,
            window.password,
            function(response){
                showScreen("profile-selection-box");
                loadProfiles();
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
    python.on('ready', function(evt) { loadProfiles(); });

    $("#add-user-button").click(function(event){
    
        showScreen("user-creation-box");

    });

    /* When user clicks a user profile, proceed with reading handshake */
    $(".profile-img").click(function(event) {

        window.email = event.target.title;

        showScreen("handshake-progress-box");

        /* READ THE HANDSHAKE */

        /* read the first handshake */
        $(".signal").css("display","none");    
        $("#signal0").css("display","block");
        console.log("#signal0");
        // Read in three symbols and append to empty array
        // Call "decode" when done reading.
        readPassword(3, decode);
    });

    /* When user submits user creation form, process it */
    $('#user-creation-form').submit(function() {

        window.fullname = $('#full-name').val();
        window.email = $('#email').val();
        window.password = $('#password').val();

        console.log(fullname);
        console.log(email);
        console.log(password);
        console.log('User creation form submitted. Now about to get handshake');
   
        showScreen("handshake-progress-box");

        readPassword(3,addUser);

        return false;
    });


});


