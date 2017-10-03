$( document ).ready(function () {

    var userFeed = new Instafeed({
        get: 'user',
        tagName: 'hybriantnu',
        userId: '1006054999',
        limit: 4,
        resolution: 'standard_resolution',
        accessToken: '1006054999.1677ed0.eacce826da234df1897c4a9f9293c1a8',
        sortBy: 'most-recent',
        template: '<div class=gallery"><a href="{{link}}" title="{{caption}}" target="_blank"><img src="{{image}}" alt="{{caption}}" class="img-fluid"/></a></div>',
    });
    userFeed.run();


});