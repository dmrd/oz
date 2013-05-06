// Copyright (c) 2012 The Chromium Authors. All rights reserved.
// Use of this source code is governed by a BSD-style license that can be
// found in the LICENSE file.

/**
 * Global variable containing the query we'd like to pass to Flickr. In this
 * case, kittens!
 *
 * @type {string}
 */
var QUERY = 'puppies';

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
    });
    
    setTimeout(function() { periodic(); }, 2000);
    
}

// Run our kitten generation script as soon as the document's DOM is ready.
document.addEventListener('DOMContentLoaded', function () {
    
    setTimeout(function() { periodic(); }, 2000);
                          
});
