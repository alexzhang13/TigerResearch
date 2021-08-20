function getFilters() {
    var boxes = document.getElementsByClassName('check');
    var queryString = "";
    for (var i=0;i<boxes.length;i++) {
        if (boxes[i].value=="1") queryString += boxes[i].id + " ";
    }
    return queryString;
}

/* Display all professors in search query on page load */
document.addEventListener('DOMContentLoaded', function() {
    var search_text = $("#listSearch").val();
    $.ajax({
        method: "post",
        url: "/livesearch",
        data: { text: search_text, qstring: "" },
        success: function (res) {
            data = ""
            /* note the outer loop is the entire array (it only has one element); may fix this later */
            /* this loop displays the search functions */
            $.each(res, function (oindex, ovalue) {
                $.each(ovalue, function (index, value) {
                    data +=
                        "<a class=\"list-group-item list-group-item-action py-3 lh-tight\" onclick=\"search_click(\'" + value.netid + "\')\" id=\"" + value.netid + "-list" +
                    "\" data-toggle=\"list\" href=\"/professor/" + value.netid + "\"" +
                    "role=\"tab\" aria-controls=\"" + value.netid + "\">" +
                    "<div class=\"flex-container-row\">" +
                        " <div class=\"flex-item-stretch truncate\"> " +
                        " <strong class=\"mb-1\">" + value.name + "</strong> " +
                        " <small>" + value.department + "</small> " + 
                        "</div>" +
                        "<div class=\"flex-item-rigid\">" + 
                        value.likes + " <span class=\"glyphicon glyphicon-heart\"></span>" +
                        " </div> " +
                    "</div>" +  
                        " <div class=\"col-10 mb-1 small\">" + value.keywords + "</div>" +
                        "</a>"
                });
                num_results = "<h3 class=\"panel-title\" style=\"color: #fff\">" + ovalue.length + " Search Results</h3>"
            });
            $("#search-results").html(data)
            $("#search-results-num").html(num_results)
            
        }
    });
}, false);

$(document).ready(function () {
    $("#listSearch").on("input", function (e) {
        var search_text = $("#listSearch").val();
        var queryString = getFilters();
        $.ajax({
            method: "post",
            url: "/livesearch",
            data: { text: search_text, qstring: queryString},
            success: function (res) {
                data = ""
                /* note the outer loop is the entire array (it only has one element); may fix this later */
                /* this loop displays the search functions */
                $.each(res, function (oindex, ovalue) {
                    $.each(ovalue, function (index, value) {
                        data +=
                            "<a class=\"list-group-item list-group-item-action py-3 lh-tight\" onclick=\"search_click(\'" + value.netid + "\')\" id=\"" + value.netid + "-list" +
                        "\" data-toggle=\"list\" href=\"/professor/" + value.netid + "\"" +
                        "role=\"tab\" aria-controls=\"" + value.netid + "\">" +
                        "<div class=\"flex-container-row\">" +
                            " <div class=\"flex-item-stretch truncate\"> " +
                            " <strong class=\"mb-1\">" + value.name + "</strong> " +
                            " <small>" + value.department + "</small> " + 
                            "</div>" +
                            "<div class=\"flex-item-rigid\">" + 
                            value.likes + " <span class=\"glyphicon glyphicon-heart\"></span>" +
                            " </div> " +
                        "</div>" +  
                            " <div class=\"col-10 mb-1 small\">" + value.keywords + "</div>" +
                            "</a>"
                    });
                    num_results = "<h3 class=\"panel-title\" style=\"color: #fff\">" + ovalue.length + " Search Results</h3>"
                });
                $("#search-results").html(data)
                $("#search-results-num").html(num_results)
            }
        })
    });
});

function tick_checkbox(button) {
    var id = button.id;
    if ($("#" + id).val() == 0) {
        $("#" + id).val(1);
    } else {
        $("#" + id).val(0);
    }
    var queryString = getFilters();
    var search_text = $("#listSearch").val();
    console.log(queryString);
    $.ajax({
        method: "post",
        url: "/livesearch",
        data: { text: search_text, qstring: queryString},
        success: function (res) {
            data = ""
            /* note the outer loop is the entire array (it only has one element); may fix this later */
            /* this loop displays the search functions */
            $.each(res, function (oindex, ovalue) {
                $.each(ovalue, function (index, value) {
                    data +=
                        "<a class=\"list-group-item list-group-item-action py-3 lh-tight\" onclick=\"search_click(\'" + value.netid + "\')\" id=\"" + value.netid + "-list" +
                        "\" data-toggle=\"list\" href=\"/professor/" + value.netid + "\"" +
                        "role=\"tab\" aria-controls=\"" + value.netid + "\">" +
                        "<div class=\"flex-container-row\">" +
                        " <div class=\"flex-item-stretch truncate\"> " +
                        " <strong class=\"mb-1\">" + value.name + "</strong> " +
                        " <small>" + value.department + "</small> " +
                        "</div>" +
                        "<div class=\"flex-item-rigid\">" +
                        value.likes + " <span class=\"glyphicon glyphicon-heart\"></span>" +
                        " </div> " +
                        "</div>" +
                        " <div class=\"col-10 mb-1 small\">" + value.keywords + "</div>" +
                        "</a>"
                });
                num_results = "<h3 class=\"panel-title\" style=\"color: #fff\">" + ovalue.length + " Search Results</h3>"
            });
            $("#search-results").html(data)
            $("#search-results-num").html(num_results)
        }
    })
}