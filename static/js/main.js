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

var feedbackVisible = false;
function toggleFeedbackBox() {
    var $sb = $('#feedbackBox');
    if (feedbackVisible) {
        $sb.css('right', '-100%');
    } else {
        $sb.css('right','0');
    }
    feedbackVisible = !feedbackVisible;
}

function submitFeedback() {

    // Get handlers
    var $button = $('#feedbackButton');
    var $content = $('#feedbackContent');

    // Get data
    var text = $content.val();
    var anonymous = $('#feedbackAnonymous').is(":checked");

    // Verify request
    if (text == "") {
      alert("Du kan ikke sende et tomt forslag.");
      return;
    }

    // Stop user from sending while waiting
    $button.prop("disabled", true);

    // Get csrf token
    var csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();

    // Send JSON post request
    $.post("/api/feedback", {ANONYMOUS: anonymous, DATA: text, csrfmiddlewaretoken: csrftoken}
    ).fail(function() {
      alert("Noe gikk galt og forslaget ble ikke sent.");
    }).done(function() {
      $content.val(""); // Reset text
      toggleFeedbackBox(); // Hide box
    }).always(function() {
      $button.prop("disabled", false); // Enable button when done waiting
    });
}
