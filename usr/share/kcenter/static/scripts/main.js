// Disable right click
if(typeof debug == 'undefined' || !debug){
    (function () {
      var blockContextMenu, myElement;

      blockContextMenu = function (evt) {
        evt.preventDefault();
      };

      myElement = document.querySelector('html');
      myElement.addEventListener('contextmenu', blockContextMenu);
    })();
}


function stringSearch(str) {
     var rExps=[
         {re:/[\xC0-\xC6]/g, ch:'A'},
         {re:/[\xE0-\xE6]/g, ch:'a'},
         {re:/[\xC8-\xCB]/g, ch:'E'},
         {re:/[\xE8-\xEB]/g, ch:'e'},
         {re:/[\xCC-\xCF]/g, ch:'I'},
         {re:/[\xEC-\xEF]/g, ch:'i'},
         {re:/[\xD2-\xD6]/g, ch:'O'},
         {re:/[\xF2-\xF6]/g, ch:'o'},
         {re:/[\xD9-\xDC]/g, ch:'U'},
         {re:/[\xF9-\xFC]/g, ch:'u'},
         {re:/[\xD1]/g, ch:'N'},
         {re:/[\xF1]/g, ch:'n'}
     ];

     for(var i=0, len=rExps.length; i<len; i++)
         str=str.replace(rExps[i].re, rExps[i].ch);

     return str.toLowerCase();
}


// element to add content
var content = $("#content");

// get apps
var data = Pyjs.getApps();
var apps = $.parseJSON(data);

var result = "";
for(var category in apps){

    result += '<div class="ui raised segment category">' +
                '<div class="ui ribbon teal label title">' + category + '</div>' +
                '<br style="clear: both" />';

    for(var item = 0; item < apps[category].length; item++){
        var app = apps[category][item];

        result += '<div class="ui basic floated left segment app" data-content="' + app.comment + '" data-variation="inverted">' +
                    '<a href="javascript:;" data-execute="' + app.execute + '">' +
                        '<div class="icon">' +
                            '<img src="' + app.icon + '" class="ui image" />' +
                        '</div>' +
                        '<div class="name">' + app.name + '</div>' +
                    '</a>' +
                    '<div class="ui active inverted dimmer"><div class="ui loader"></div></div>' +
                  '</div>';

    }

    result += '</div>';
}

content.append(result);

// tooltip
$("div.app").popup({
    delay: 200,
    duration: 100
});

// launcher
$(".app a").on("click", function(){

    // elements
    var elem = $(this);
    var execute = elem.data("execute");
    var body = $("body");

    body.addClass("load");
    elem.addClass("load");

    // execute
    Pyjs.cmd(execute);

    // hide loader
    setTimeout(function(){
        body.removeClass("load");
        elem.removeClass("load");
    }, 2000);

});

// search
var apps = $(".app");
$("#search").on("input", function(e){
    var elem = $(this);
    if(elem.val().length == 0){
        apps.show().parent().show();
    }
    else{
        apps.each(function(){

            var category = $(this).parent();
            var sContent = stringSearch($(this).data("content"));
            var sSearch = stringSearch(elem.val().trim());
            var sName = stringSearch($(this).find("div.name").text());

            if(sContent.indexOf(sSearch) != -1 || sName.indexOf(sSearch) != -1){
                $(this).show();
                category.show();
            }
            else{
                $(this).hide();
            }

            if(category.find(".app:visible").length > 0){
                category.show();
            }
            else{
                category.hide();
            }

        });
    }
});