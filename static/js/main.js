_=function(o){return function(){return o;}};

String.prototype.replaceAll = function(replacing, replacement) {
    return this.replace(new RegExp(replacing, 'g'), replacement);
}

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

function toggleSuggestionBox() {
    var $sb = $('#suggestionBox');
    $sb.css('right', $sb.css('right') == '16px' ? '-100%' : 16);
}

function submitSuggestion() {
    var $button = $('#suggestionBox #suggestionButton');
    var $suggestion = $('#suggestionBox #suggestionContent');

    var title = window.location.href;
    var suggestingUser = $('#suggestionBox #suggestingUser').val();
    var anonymously = $('#suggestionBox #suggestAnonymously').is(":checked");

    var jsonSafe = function(string) {
        return string.replaceAll('\\\\', '\\\\').replaceAll('"', '\\"');
    };

    var pretext;
    if (anonymously || suggestingUser == "") {pretext = "Nytt anonymt forslag!"}
    else {pretext = "Nytt forslag fra "+suggestingUser+"!"}

    $button.prop('disabled', true);
    $.post("https://hooks.slack.com/services/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", 'payload={"attachments":[{\
        "fallback":     "Nytt forslag til forbedring!",\
        "pretext":      "' + jsonSafe(pretext) + '",\
        "color":        "good",\
        "fields":[{\
            "title":    "' + jsonSafe(title) + '",\
            "value":    "' + jsonSafe($suggestion.val()) + '",\
            "short":    false\
    }]}]}').fail(function() {
        alert("Noe gikk galt og forslaget ble ikke sent.");
    }).done(function() {
        $suggestion.val('');
        toggleSuggestionBox();
    }).always(function() {
        $button.prop('disabled', false);
    });
}