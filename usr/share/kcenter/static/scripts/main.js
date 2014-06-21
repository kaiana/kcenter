// disable right click
(function () {
  var blockContextMenu, myElement;

  blockContextMenu = function (evt) {
    evt.preventDefault();
  };

  myElement = document.querySelector('body');
  myElement.addEventListener('contextmenu', blockContextMenu);
})();


var appBind = function(){

    $(".app a").on("click", function(){

        // get app to execute
        var exec = $(this).data("exec");

        // show loader
        var loader = $(this).next();
        loader.show();

        // execute
        Pyjs.run_kde("kcmshell4 " + exec);

        // hide loader
        setTimeout(function(){
            loader.hide();
        }, 1000);

    });

}


// routes
Sammy('#main', function() {

    // element to add content
    var content = this.$element();

    // default route
    this.get('#/', function() {

        var data = Pyjs.getApps();
        var apps = $.parseJSON(data);
        console.log(data);

        var result = "";
        for(var category in apps){

            result += '<div class="ui raised segment category">' +
                        '<div class="ui ribbon teal label title">' + category + '</div>' +
                        '<br style="clear: both" />';

            for(var item = 0; item < apps[category].length; item++){
                var app = apps[category][item];

                result += '<div class="ui basic floated left segment app">' +
                            '<a href="javascript:;" data-exec="' + app.filename + '">' +
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
        appBind();

    });


}).run();