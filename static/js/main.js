_=function(o){return function(){return o;}};

String.prototype.replaceAll = function(replacing, replacement) {
    return this.replace(new RegExp(replacing, 'g'), replacement);
};

clearSelf = function(obj) {
    obj.innerHTML="";
};
clearSelfValue = function(obj) {
    obj.value="";
};
hideMessage = function(obj) {
    obj.style.animation = obj.style.WebkitAnimation = "message-hide 1s";
    obj.style.animationFillMode = obj.style.WebkitAnimationFillMode = "forwards";
};

uploadFile = function(file, success, uploadFolder) {
    var formData = new FormData();
    formData.append("file", file);
    $.ajax({
        url: "/api/upload" + (uploadFolder != null ? "/" + uploadFolder : ""),
        type: "POST",
        data: formData,
        cache: false,
        contentType: false,
        processData: false,
        success: success
    });
};

calculateSuperCenter = function(){
    $(".super-center").each(function(i){
        var elem = $(this);
        elem.css({"position": "relative", "transform": "translate(-50%, -50%)"});
        var parent = elem.parent();
        elem.css("left", parent.width()/2);
        var wait = 0;
        if(parent.height() == 0) wait = 200;
        setInterval(function(){
            elem.css("top", parent.height()/2);
        }, wait);
    });
};

$(function() {
    calculateSuperCenter();
});

$(document).ready(function() {
    calculateSuperCenter();
    $(window).resize(calculateSuperCenter);
});

function toggleFeedbackBox() {
    var $sb = $('#feedbackBox');
    if ($sb.css('right') == '16px') {
        $sb.css('right', '-8px'); // Account for shadow on box
        $sb.css('transform', 'translateX(100%)');
    } else {
        $sb.css('right','16px');
        $sb.css('transform', 'translateX(0)');
    }
}

function submitFeedback() {

    // Get handlers
    var $button = $('#feedbackButton');
    var $content = $('#feedbackContent');

    // Get data
    var url = window.location.href;
    var content = $content.val();
    var user = $('#feedbackUser').val();
    var email = $('#feedbackEmail').val();
    var anonymous = $('#feedbackAnonymous').is(":checked");

    // Email data
    var subject = "Tilbakemelding til Vevkom";
    var bodyPreText = "Dette er et svar på din tilbakemelding:\n"

    // Format data
    var slackSafe = function(string) {
        return $.trim(string.replaceAll('&', '&amp;')
                            .replaceAll('<', '&lt;')
                            .replaceAll('>', '&gt;'));
    };

    var urlWithParams = function(url, params) {
        var params_str = [];
        for (var param in params) {
            params_str.push(param + '=' + encodeURIComponent(params[param]));
        }
        return url + '?' + params_str.join('&');
    };

    var fallback = "Feedback received";
    var authorName = anonymous ? "" : slackSafe(user);
    var authorLink = anonymous ? "" : encodeURI("mailto:" + email + "?subject=") + encodeURIComponent(subject) + encodeURI("&body=") + encodeURIComponent(bodyPreText + content);
    var authorIcon = "https://slack-files.com/T0CAJ0U4A-F2WLMK087-7d8bf05908";
    var color = "good";
    var sentFromUrl = "Sent from " + url;
    var issueUrl = "Generate issue: " + urlWithParams(window.location.origin + "/gitlab/ny", {"a": authorName, "t": Math.floor(Date.now() / 1000), "m": slackSafe(content), "u": url});
    var text = slackSafe(content);

    // Verify request
    if (text == "") {
      alert("Du kan ikke sende et tomt forslag.");
      return;
    }

    // Stop user from sending while waiting
    $button.prop("disabled", true);

    // Send JSON post request
    $.post("https://hooks.slack.com/services/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", JSON.stringify({
      "attachments": [
        {
          "fallback": fallback,
          "author_name": authorName,
          "author_link": authorLink,
          "author_icon": authorIcon,
          "color": color,
          "footer": sentFromUrl + "\n" + issueUrl,
          "text": text
        }
      ]
    })).fail(function() {
      alert("Noe gikk galt og forslaget ble ikke sent.");

    }).done(function() {
      $content.val(""); // Reset text
      toggleFeedbackBox(); // Hide box

    }).always(function() {
      $button.prop("disabled", false); // Enable button when done waiting
    });
}
