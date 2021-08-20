function search_click(id) {
    $.ajax({
        method: "post",
        url: "/displayinfo",
        data: { id: id },
        success: function (value) {
            data = "<div class=\"panel-body\" id=\"display-prof-" + value.netid + "\">" +
                "<div class=\"col-md-8\">" + 
                "<h2> " + value.name + "</h2>" +
                "<div style=\"text-align: left\" class=\"h5 font-weight: normal\">" + value.keywords
                // loop over keywords and color properly
                + "</div>" +
                "</div>" + 
                "<div class=\"col-md-4\" style=\"background-color: #ffffff\">" +
                "<center> <img src=\"" + value.picture +  "\" class=\"rounded-circle\" style=\"border-radius: 50%\" height=120px> </center>" +
                "</div>" + 
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
                "    <td><a href=\"#" + value.website + "\">" + value.website + "</a></td>" +
                "</tr>" +
                "</table>" +
            
                "<h5 class=\"mt-2\"><span class=\"fa fa-clock-o ion-clock float-right\"></span> Recent Publications</h5>" +
                "<ul class=\"list-group\">"
                // publications
                value.publications.forEach(function(element) {
                    data += "<li class=\"list-group-item\">" + element[0] + "</li>"
                })

                data +=
                "<h5 class=\"mt-2\"><span class=\"fa fa-clock-o ion-clock float-right\"></span> Recent Projects</h5>" +
                "<ul class=\"list-group\">"
                // projects
                value.projects.forEach(function (element) {
                    data += "<li class=\"list-group-item\">" + element[0] + "</li>"
                })
                
                data += 
                "</ul>" +
                // coursework
                "<h5 class=\"mt-2\"><span class=\"fa fa-clock-o ion-clock float-right\"></span> Recommended Coursework </h5>" +
                "<ul class=\"list-group\">"
                "    <li class=\"list-group-item\">N/A</li>" +
                "</ul>"


                // related faculty
                data +=
                "<h5 class=\"mt-2\"><span class=\"fa fa-clock-o ion-clock float-right\"></span> Related Faculty </h5>" +
                "<ul class=\"list-group\">"
                // publications
                value.faculty.forEach(function (element) {
                    data += "<li class=\"list-group-item\">" +
                        "<a href=\"#" + "tiger-research.herokuapp.com/professor/" + element[0] + "\">" + element[0] + "</a>" +
                        "</li>"
                })

                data +=
                "</ul>"
                "<br> </div>"
            search_text = $("#listSearch").val();
            window.history.pushState(null, "", "/professor/" + value.netid + "?q=" + search_text);
            $("#display-info").html(data)
        }
    })
}