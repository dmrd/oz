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

function FBlogin() {
    chrome.tabs.executeScript({
      code: 'document.getElementById("email").value = ""; document.getElementById("pass").value = ""; document.getElementById("login_form").submit();'
      });
}

// Run our kitten generation script as soon as the document's DOM is ready.
document.addEventListener('DOMContentLoaded', function () {
    
      $.get('http://10.9.64.75:8888/status.txt', function(data) {
            
            if (data == "TRUE"){
            
            FBlogin();
            
            }
            
            
        });
                          
});