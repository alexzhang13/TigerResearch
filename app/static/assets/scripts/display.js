function hash_color (text) {
    var hash = 0;
    for (var i = 0; i < text.length; i++) {
        hash = text.charCodeAt(i) + ((hash << 7) - hash);
    }
    var color = "";
    for (var i = 0; i < 3; i++) {
        var value = (hash >> (i * 8)) & 0xFF;
        color += ('00' + value.toString(16)).substr(-2)
    }
    return color;
}

function search_click(id) {
    $.ajax({
        method: "post",
        url: "/displayinfo",
        data: { id: id },
        success: function (value) {
            data = "<div class=\"panel-body\" id=\"display-prof-" + value.netid + "\">" +
                "<div class=\"container\">" +
                "<div class=\"col-md-9\">" + 
                "<h2> " + value.name + "</h2>" +
                "<div style=\"text-align: left\" class=\"h5 font-weight: normal\">"
                value.fingerprints.forEach(function (element) {
                    data += "<span class=\"badge\" style=\"margin: 0.3em; background-color: #" + hash_color(element[0]) +  " \">" + element[0] + "</span>"
                })
                // loop over keywords and color properly
                data += "</div>" +
                "</div>" + 
                "<div class=\"col-md-3\" style=\"background-color: #ffffff\">" +
                "<center> <img src=\"" + value.picture +  "\" class=\"rounded-circle\" style=\"border: 1px solid; border-radius: 20%\" height=120px> </center>" +
                "</div>" +
                "</div>"

                data +=
                "<br>" + 
                "<hr>" + 
                "<table class=\"table table-hover table-sm table-properties\">" +
                "<tr v-show=\"department\">" +
                "    <th>Department: </th>" +
                "    <td style=\"white-space: nowrap; overflow: hidden; text-overflow: ellipsis; max-width: 20rem;\">" + value.department + "</td>" +
                "</tr>" +
                "<tr v-show=\"available\">" +
                "    <th>Status: </th>" +
                "    <td style=\"white-space: nowrap; overflow: hidden; text-overflow: ellipsis; max-width: 20rem;\">Available for IW/Thesis Advising</td>" +
                "</tr>" +
                "<tr v-show=\"email\">" +
                "    <th>Email:</th>" +
                "    <td>" + value.email + "</td>" +
                "</tr>" +
                "<tr v-show=\"website\">" +
                "    <th>Website:</th>" +
                "    <td><a href=\"" + value.website + "\">" + value.website + "</a></td>" +
                "</tr>" +
                "</table>" +
                "<hr>" +
                "<h5 class=\"mt-2\"><span class=\"fa fa-clock-o ion-clock float-right\"></span> Recent Publications</h5>" +
                "<ul class=\"list-group\">"
                // publications
                value.publications.forEach(function(element) {
                    data += "<li class=\"list-group-item\">" + element[0] + "</li>"
                })

                data +=
                "</ul>" +
                "<hr>" +
                "<h5 class=\"mt-2\"><span class=\"fa fa-clock-o ion-clock float-right\"></span> Recent Projects</h5>" +
                "<ul class=\"list-group\">"
                // projects
                value.projects.forEach(function (element) {
                    data += "<li class=\"list-group-item\">" + element[0] + "</li>"
                })
                
                data += 
                "</ul>" +
                // coursework
                "<hr>" +
                "<h5 class=\"mt-2\"><span class=\"fa fa-clock-o ion-clock float-right\"></span> Recommended/Taught Coursework </h5>" +
                "<ul class=\"list-group\">" +
                "    <li class=\"list-group-item\">N/A</li>" +
                "</ul>"


                // related faculty
                data +=
                "<hr>" +
                "<h5 class=\"mt-2\"><span class=\"fa fa-clock-o ion-clock float-right\"></span> Related Faculty </h5>" +
                "<ul class=\"list-group\">"
                value.faculty.forEach(function (element) {
                    data += "<li class=\"list-group-item\">" +
                        "<a href=\"" + "tiger-research.herokuapp.com/professor/" + element[0] + "\">" + element[0] + "</a>" +
                        "</li>"
                })

                data +=
                "</ul>" +
                "<hr> <br> </div>"
            search_text = $("#listSearch").val();
            window.history.pushState(null, "", "/professor/" + value.netid + "?q=" + search_text);
            $("#display-info").html(data)
        }
    })
}

function load_profile(id) {
    console.log("ong load")
    $.ajax({
        method: "post",
        url: "/displayinfo",
        data: { id: id },
        success: function (value) {
            data = "<div class=\"panel-body\" id=\"display-prof-" + value.netid + "\">" +
                "<div class=\"container\">" +
                "<div class=\"col-md-9\">" +
                "<h2> " + value.name + "</h2>" +
                "<div style=\"text-align: left\" class=\"h5 font-weight: normal\">"
            value.fingerprints.forEach(function (element) {
                data += "<span class=\"badge\" style=\"margin: 0.3em; background-color: #" + hash_color(element[0]) + " \">" + element[0] + "</span>"
            })
            // loop over keywords and color properly
            data += "</div>" +
                "</div>" +
                "<div class=\"col-md-3\" style=\"background-color: #ffffff\">" +
                "<center> <img src=\"" + value.picture + "\" class=\"rounded-circle\" style=\"border: 1px solid; border-radius: 20%\" height=120px> </center>" +
                "</div>" +
                "</div>"

            data +=
                "<br>" +
                "<hr>" +
                "<table class=\"table table-hover table-sm table-properties\">" +
                "<tr v-show=\"department\">" +
                "    <th>Department: </th>" +
                "    <td style=\"white-space: nowrap; overflow: hidden; text-overflow: ellipsis; max-width: 20rem;\">" + value.department + "</td>" +
                "</tr>" +
                "<tr v-show=\"available\">" +
                "    <th>Status: </th>" +
                "    <td style=\"white-space: nowrap; overflow: hidden; text-overflow: ellipsis; max-width: 20rem;\">Available for IW/Thesis Advising</td>" +
                "</tr>" +
                "<tr v-show=\"email\">" +
                "    <th>Email:</th>" +
                "    <td>" + value.email + "</td>" +
                "</tr>" +
                "<tr v-show=\"website\">" +
                "    <th>Website:</th>" +
                "    <td><a href=\"" + value.website + "\">" + value.website + "</a></td>" +
                "</tr>" +
                "</table>" +
                "<hr>" +
                "<h5 class=\"mt-2\"><span class=\"fa fa-clock-o ion-clock float-right\"></span> Recent Publications</h5>" +
                "<ul class=\"list-group\">"
            // publications
            value.publications.forEach(function (element) {
                data += "<li class=\"list-group-item\">" + element[0] + "</li>"
            })

            data +=
                "</ul>" +
                "<hr>" +
                "<h5 class=\"mt-2\"><span class=\"fa fa-clock-o ion-clock float-right\"></span> Recent Projects</h5>" +
                "<ul class=\"list-group\">"
            // projects
            value.projects.forEach(function (element) {
                data += "<li class=\"list-group-item\">" + element[0] + "</li>"
            })

            data +=
                "</ul>" +
                // coursework
                "<hr>" +
                "<h5 class=\"mt-2\"><span class=\"fa fa-clock-o ion-clock float-right\"></span> Recommended/Taught Coursework </h5>" +
                "<ul class=\"list-group\">" +
                "    <li class=\"list-group-item\">N/A</li>" +
                "</ul>"


            // related faculty
            data +=
                "<hr>" +
                "<h5 class=\"mt-2\"><span class=\"fa fa-clock-o ion-clock float-right\"></span> Related Faculty </h5>" +
                "<ul class=\"list-group\">"
            value.faculty.forEach(function (element) {
                data += "<li class=\"list-group-item\">" +
                    "<a href=\"" + "tiger-research.herokuapp.com/professor/" + element[0] + "\">" + element[0] + "</a>" +
                    "</li>"
            })

            data +=
                "</ul>" +
                "<hr> <br> </div>"
            $("#display-info").html(data)
        }
    })
}