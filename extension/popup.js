var gotGesture = false;
var gestures = new Array();
var email = "";
var fullname = "";
var password = "";
var confirmation_code = 31140;

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
                console.log("Email: " + email);
                console.log("Fullname: " + fullname);
                $("#profile-selection-box").append('<div class="profile"><img style="height:50px;" class="profile-img" title="'+email+'" src="facebook-man.jpeg"></img><br />'+fullname+'</div>');
            }
            
            /* When user clicks a user profile, proceed with reading handshake */
            $(".profile-img").click(function(event) {

                window.email = event.target.title;
                console.log("Email: " + window.email);
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
            gestures,
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
                //reload the extension
                   location.reload();
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

    
    $("#reset-handshake-button").click(function(event){
    
        showScreen("handshake-reset-box");

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

    /* When user sends password reset email address, we send them text confirmation */
    $('#handshake-reset-form').submit(function() {

        email = $('#reset-email').val();
        console.log('Resetting handshake for '+email);
    
        python.sendText(window.confirmation_code,function(response){var blah = true;});
        
        $("#handshake-reset-form").css("display","none");
        $("#handshake-reset-code-form").css("display","block");

        return false;
    });


    /* Handle confirmation code */
    $('#handshake-reset-code-form').submit(function() {

        code = $('#confirmation-code').val();
        window.password = $('#reset-fb-password').val();
        
        if (code != window.confirmation_code){
            alert("Codes do not match.");
        } else {
            showScreen("handshake-progress-box");
            python.getName(window.email, function(response){ 
                        window.fullname = response;
                        readPassword(3,addUser);
            });
            //readPassword(3,addUser);
        }

        return false;
    });


});


