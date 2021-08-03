$(document).ready(function () {
    $("#listSearch").on("input", function (e) {
        search_text = $("#listSearch").val();
        $.ajax({
            method: "post",
            url: "/livesearch",
            data: { text: search_text },
            success: function (res) {
                data = ""
                console.log(res)
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
                });
                $("#search-results").html(data)
            }
        })
    });
})