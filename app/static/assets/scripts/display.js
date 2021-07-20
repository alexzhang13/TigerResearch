function search_click(id) {
    console.log(id);
    $.ajax({
        method: "post",
        url: "/displayinfo",
        data: { id: id },
        success: function (value) {
            data = "<div class=\"panel-body\" id=\"display-prof-" + value.id + "\">" +
                "<center> <h2> <span style=\"color:gray\">Professor</span> " + value.name + "</h2> </center>" +
                "<div style=\"text-align: center\" class=\"h5 font-weight-300\">" + value.keywords + "</div>" +
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
                "    <th>Email</th>" +
                "    <td>" + value.email + "</td>" +
                "</tr>" +
                "<tr v-show=\"website\">" +
                "    <th>Website</th>" +
                "    <td><a href=\"#" + value.website + "\">" + value.website + "</a></td>" +
                "</tr>" +
                "</table>" +
                "<h5 class=\"mt-2\"><span class=\"fa fa-clock-o ion-clock float-right\"></span> Recent Publications</h5>" +
                "<ul class=\"list-group\">" +
                "    <li class=\"list-group-item\">Default 1</li>" +
                "    <li class=\"list-group-item\">Default 2</li>" +
                "    <li class=\"list-group-item\">Default 3</li>" +
                "</ul>" +
                "</div>"
            console.log(data);
            $("#display-info").html(data)
        }
    })
}