
function displayStats() {
    //Prevent browser cache
    $.getJSON('get/stats?' + Math.floor(Math.random()*30000), function (data) {
        var x = "";
        var z = "";

        for (var entry in data) {
            //It works okay...
            if( entry == "Rounds Played" || entry == "Players Revived") {
                z += "<span class=\"btn btn-success btn-override\">" +
                entry + "<em>" + data[entry] + "</em></span>";
                $('#zombies-stats').html(z);

            } else
            x += "<span class=\"btn btn-success btn-override\">" +
                entry + "<em>" + data[entry] + "</em></span>";
        }
            $('#stats').html(x);

    });
}

$(document).ready(function () {
    displayStats();
});